# client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Generic BLE Client definition that is composed of a BLE Controller."""

import re
import logging
from pathlib import Path
from typing import Generic, Optional, Union, Pattern, Type, Tuple, List

from open_gopro.ble import BleUUID
from open_gopro.exceptions import FailedToFindDevice, ConnectFailed
from .controller import (
    BLEController,
    BleDevice,
    BleHandle,
    DisconnectHandlerType,
    NotiHandlerType,
)
from .services import GattDB, BleUUID, UUIDs

logger = logging.getLogger(__name__)


class BleClient(Generic[BleHandle, BleDevice]):
    """A BLE device that is to be connected to."""

    def __init__(
        self,
        controller: BLEController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: Tuple[Union[Pattern, BleDevice], Optional[List[BleUUID]]],
        uuids: Optional[Type[UUIDs]] = None,
    ) -> None:
        """Constructor

        Args:
            controller (BLEController): controller implementation to use for this client
            disconnected_cb (DisconnectHandlerType): disconnected callback
            notification_cb (NotiHandlerType): notification callback
            target (Tuple[Union[Pattern, BleDevice], Optional[List[BleUUID]]]): Tuple of (device, service_uuids)
                where device is the BleDevice (or regex) to connect to and service_uuids is a list of
                service uuid's to filter for
            uuids (Type[UUIDs], optional): Additional UUIDs that will be used when discovering characteristic.
                Defaults to None in which case any unknown UUIDs will be set to "unknown".

        Raises:
            ValueError: Must pass a valid target
        """
        if target is None:
            raise ValueError("Target can not be None!")
        if isinstance(target[0], str):
            self._target = re.compile(target[0])
        else:
            self._target = target[0]  # type: ignore
        self._service_uuids: List[BleUUID] = target[1] or []
        self._controller = controller
        self._disconnected_cb = disconnected_cb
        self._notification_cb = notification_cb
        self._gatt_table: Optional[GattDB] = None
        self._device: Optional[BleDevice] = None
        self._handle: Optional[BleHandle] = None
        self._identifier: Optional[str] = None if isinstance(self._target, Pattern) else str(self._target)
        self.uuids = uuids

    def _find_device(self, timeout: int = 5, retries: int = 30) -> None:
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
                self._device = self._controller.scan(self._target, timeout, self._service_uuids)
                return
            except FailedToFindDevice as e:
                logger.warning(f"Failed to find a device in {timeout} seconds. Retrying #{retry}")
                if retry == retries - 1:
                    raise FailedToFindDevice from e

    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Open the client resource so that it is ready to send and receive data.

        Args:
            timeout (int): How long to try connecting (in seconds) before retrying. Defaults to 10.
            retries(int): How many retries to attempt before giving up. Defaults to 5

        Raises:
            ConnectFailed: The BLE connection was not able to establish
        """
        # If we need we need to find the device to connect
        if isinstance(self._target, Pattern):
            self._find_device()
        # Otherwise we already have it
        else:
            self._device = self._target
        self._identifier = str(self._device)

        logger.info("Establishing the BLE connection")
        for retry in range(retries):
            try:
                self._handle = self._controller.connect(self._disconnected_cb, self._device, timeout=timeout)
                break
            except ConnectFailed as e:
                logger.warning(f"Failed to connect. Retrying #{retry}")
                if retry == retries - 1:
                    raise ConnectFailed("BLE", timeout, retries) from e

        assert self._handle is not None
        # Attempt to pair
        self._controller.pair(self._handle)
        # Discover characteristics
        self._gatt_table = self._controller.discover_chars(self._handle, self.uuids)
        # Enable all GATT notifications
        self._controller.enable_notifications(self._handle, self._notification_cb)

    def close(self) -> None:
        """Close the client resource.

        This should always be called before exiting.
        """
        if self.is_connected:
            logger.info("Terminating the BLE connection")
            self._controller.disconnect(self._handle)
            self._handle = None
        else:
            logger.debug("BLE already disconnected")

    def read(self, uuid: BleUUID) -> bytearray:
        """Read byte data from a characteristic (identified by BleUUID)

        Args:
            uuid (BleUUID): characteristic to read

        Returns:
            bytearray: byte data that was read
        """
        return self._controller.read(self._handle, uuid)

    def write(self, uuid: BleUUID, data: bytearray) -> None:
        """Write byte data to a characteristic (identified by BleUUID)

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): byte data to write
        """
        self._controller.write(self._handle, uuid, data)

    @property
    def gatt_db(self) -> GattDB:
        """Return the attribute table

        Returns:
            GattDB: table of BLE attributes
        """
        if self._gatt_table is None:
            # Discover characteristics
            assert self._handle is not None
            self._gatt_table = self._controller.discover_chars(self._handle)
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
