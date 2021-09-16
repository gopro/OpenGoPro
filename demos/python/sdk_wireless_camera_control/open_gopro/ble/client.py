# client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Generic BLE Client definition that is composed of a BLE Controller."""

import re
import csv
import logging
from pathlib import Path
from typing import Generic, Optional, Union, Pattern

from open_gopro.exceptions import FailedToFindDevice, ConnectFailed
from .controller import (
    BLEController,
    BleDevice,
    BleHandle,
    DisconnectHandlerType,
    NotiHandlerType,
)
from .services import AttributeTable

logger = logging.getLogger(__name__)


class BleClient(Generic[BleHandle, BleDevice]):
    """A BLE client that is composed of, among other things, a BLE interface

    The interface is generic and can be set with the 'controller' argument
    """

    def __init__(
        self,
        controller: BLEController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: Union[Pattern, BleDevice],
    ) -> None:
        if target is None:
            raise ValueError("Target can not be None!")
        if isinstance(target, str):
            # TODO is there a way to check if target is BleDevice?
            target = re.compile(target)
        self._controller = controller
        self._disconnected_cb = disconnected_cb
        self._notification_cb = notification_cb
        self._target = target
        self._gatt_table: Optional[AttributeTable] = None
        self._device: Optional[BleDevice] = None
        self._handle: Optional[BleHandle] = None
        self._identifier = None if isinstance(target, Pattern) else str(target)

    def __del__(self) -> None:
        logger.debug("In destructor...")
        self.close()

    def _find_device(self, timeout: int = 5, retries: int = 30) -> None:
        self._device = None
        assert isinstance(self._target, Pattern)
        for retry in range(1, retries):
            try:
                self._device = self._controller.scan(self._target, timeout)
                return
            except FailedToFindDevice as e:
                logger.warning(f"Failed to find a device in {timeout} seconds. Retrying #{retry}")
                if retry == retries - 1:
                    raise FailedToFindDevice from e

    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Open the client resource so that it is ready to send and receive data.

        Args:
            timeout (int, optional): How long to try connecting (in seconds) before retrying. Defaults to 10.
            retries(int, optional): How many retries to attempt before giving up. Defaults to 5
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
                logger.warning(f"Failed to connect in {timeout} seconds. Retrying #{retry}")
                if retry == retries - 1:
                    raise ConnectFailed("BLE", timeout, retries) from e

        assert self._handle is not None
        # Attempt to pair
        self._controller.pair(self._handle)
        # Discover characteristics
        self._gatt_table = self._controller.discover_chars(self._handle)
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

    def read(self, uuid: str) -> bytearray:
        """Read byte data from a characteristic (identified by UUID)

        Args:
            uuid (str): characteristic to read

        Returns:
            bytearray: byte data that was read
        """
        return self._controller.read(self._handle, uuid)

    def write(self, uuid: str, data: bytearray) -> None:
        """Write byte data to a characteristic (identified by UUID)

        Args:
            uuid (str): characteristic to write to
            data (bytearray): byte data to write
        """
        self._controller.write(self._handle, uuid, data)

    @property
    def gatt_table(self) -> AttributeTable:
        """Return the attribute table

        Returns:
            AttributeTable: table of BLE attributes
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

    def services_as_csv(self, dump_file: Path = Path("services.csv")) -> None:
        """Dump the services as a .csv

        Args:
            dump_file (Path, optional): Where to dump the csv. Defaults to Path("services.csv").
        """
        assert self.gatt_table is not None
        with open(dump_file, mode="w") as f:
            logger.debug(f"Dumping discovered BLE characteristics to {dump_file}")
            w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["handle", "description", "UUID", "properties", "value"])
            # For each service in table
            for s in self.gatt_table.services.values():  # type: ignore
                w.writerow(["SERVICE", s.name, s.uuid.value, "SERVICE", "SERVICE"])
                # For each characteristic in service
                for c in s.chars.values():
                    w.writerow([c.handle, c.name, c.uuid.value, " ".join(c.props), c.value])
                    # For each descriptor in characteristic
                    for d in c.descriptors:
                        w.writerow([d.handle, "DESCRIPTOR", "", "", d.value])
