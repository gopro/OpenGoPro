# client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Generic BLE Client definition that is composed of a BLE Controller."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Generic, Optional, Pattern

from open_gopro.domain.exceptions import ConnectFailed, FailedToFindDevice
from open_gopro.network.ble import BleUUID

from .controller import (
    BLEController,
    BleDevice,
    BleHandle,
    DisconnectHandlerType,
    NotiHandlerType,
)
from .services import BleUUID, GattDB, UUIDs

logger = logging.getLogger(__name__)


class BleClient(Generic[BleHandle, BleDevice]):
    """A BLE device that is to be connected to.

    Args:
        controller (BLEController): controller implementation to use for this client
        disconnected_cb (DisconnectHandlerType): disconnected callback
        notification_cb (NotiHandlerType): notification callback
        target (tuple[Pattern | BleDevice, list[BleUUID] | None]): Tuple of:
            (device, service_uuids) where device is the BLE device (or regex) to connect to and
            service_uuids is a list of service uuid's to filter for
        uuids (type[UUIDs] | None): Additional UUIDs that will be used when discovering characteristic.
            Defaults to None in which case any unknown UUIDs will be set to "unknown".

    Raises:
        ValueError: Must pass a valid target
    """

    def __init__(
        self,
        controller: BLEController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: tuple[Pattern | BleDevice, list[BleUUID] | None],
        uuids: type[UUIDs] | None = None,
    ) -> None:
        if target is None:
            raise ValueError("Target can not be None!")
        self._target: Pattern
        if isinstance(target[0], str):
            self._target = re.compile(target[0])
        else:
            self._target = target[0]  # type: ignore
        self._service_uuids: list[BleUUID] = target[1] or []
        self._controller = controller
        self._disconnected_cb = disconnected_cb
        self._notification_cb = notification_cb
        self._gatt_table: Optional[GattDB] = None
        self._device: Optional[BleDevice] = None
        self._handle: Optional[BleHandle] = None
        self._identifier: Optional[str] = self._target.pattern
        self.uuids = uuids

    async def _find_device(self, timeout: int = 5, retries: int = 30) -> None:
        """Scan for the target device.

        Args:
            timeout (int): how long (seconds) to scan before considering the attempt a failure. Defaults to 5.
            retries (int): How many attempts before giving up. Defaults to 30.

        Raises:
            FailedToFindDevice: No matching device was found
        """
        self._device = None
        assert isinstance(self._target, Pattern)
        for retry in range(1, retries):
            try:
                self._device = await self._controller.scan(self._target, timeout, self._service_uuids)
                return
            except FailedToFindDevice:
                logger.warning(f"Failed to find a device in {timeout} seconds. Retrying #{retry}")
        raise FailedToFindDevice

    async def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Open the client resource so that it is ready to send and receive data.

        Args:
            timeout (int): How long to try connecting (in seconds) before retrying. Defaults to 10.
            retries(int): How many retries to attempt before giving up. Defaults to 5

        Raises:
            ConnectFailed: The BLE connection was not able to establish
        """
        # If we need we need to find the device to connect
        if isinstance(self._target, Pattern):
            await self._find_device(timeout, retries)
        # Otherwise we already have it
        else:
            self._device = self._target
        self._identifier = str(self._device)

        logger.info("Establishing the BLE connection")
        for retry in range(1, retries):
            try:
                self._handle = await self._controller.connect(self._disconnected_cb, self._device, timeout=timeout)
                break
            except ConnectFailed as e:
                logger.warning(f"Failed to connect. Retrying #{retry}")
                if retry == retries - 1:
                    raise ConnectFailed("BLE", timeout, retries) from e

        assert self._handle is not None
        # Attempt to pair
        await self._controller.pair(self._handle)
        # Discover characteristics
        self._gatt_table = await self._controller.discover_chars(self._handle, self.uuids)
        # Enable all GATT notifications
        await self._controller.enable_notifications(self._handle, self._notification_cb)

    async def close(self) -> None:
        """Close the client resource.

        This should always be called before exiting.
        """
        if self.is_connected:
            logger.info("Terminating the BLE connection")
            await self._controller.disconnect(self._handle)
            self._handle = None
        else:
            logger.warning("BLE already disconnected")

    async def read(self, uuid: BleUUID) -> bytes:
        """Read byte data from a characteristic (identified by BleUUID)

        Args:
            uuid (BleUUID): characteristic to read

        Returns:
            bytes: byte data that was read
        """
        return await self._controller.read(self._handle, uuid)

    async def write(self, uuid: BleUUID, data: bytes) -> None:
        """Write byte data to a characteristic (identified by BleUUID)

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytes): byte data to write
        """
        await self._controller.write(self._handle, uuid, data)

    @property
    def gatt_db(self) -> GattDB:
        """Return the attribute table

        Raises:
            RuntimeError: GATT table hasn't been discovered

        Returns:
            GattDB: table of BLE attributes
        """
        if not self._gatt_table:
            raise RuntimeError("GATT table has not yet been discovered")
        return self._gatt_table

    @property
    def identifier(self) -> Optional[str]:
        """A string that identifies the GoPro

        Returns:
            Optional[str]: identifier or None if client has not yet been discovered
        """
        return self._identifier

    @property
    def is_connected(self) -> bool:
        """Is BLE currently connected?

        Returns:
            bool: True if yes, False if no
        """
        return self._handle is not None

    @property
    def is_discovered(self) -> bool:
        """Has the target been discovered (via BLE scanning)?

        Returns:
            bool: True if yes, False if no
        """
        return self._device is not None

    def services_as_csv(self, file: Path = Path("services.csv")) -> None:
        """Dump the services as a .csv

        Args:
            file (Path): Where to dump the csv. Defaults to Path("services.csv").
        """
        assert self.gatt_db is not None
        self.gatt_db.dump_to_csv(file)
