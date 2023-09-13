# controller.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""BLE Controller Interface Definition."""

import logging
from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, Pattern, TypeVar

from .services import BleUUID, GattDB, UUIDs

logger = logging.getLogger(__name__)

BleDevice = TypeVar("BleDevice")
BleHandle = TypeVar("BleHandle")
NotiHandlerType = Callable[[int, bytearray], None]
DisconnectHandlerType = Callable[[BleDevice], None]


class BLEController(ABC, Generic[BleDevice, BleHandle]):
    """Interface definition for a BLE driver to be used by GoPro."""

    def __init__(self, exception_handler: Optional[Callable] = None) -> None:
        self._exception_handler = exception_handler

    @abstractmethod
    async def read(self, handle: BleHandle, uuid: BleUUID) -> bytearray:
        """Read a bytestream response from a BleUUID.

        Args:
            handle (BleHandle): handle to pair to
            uuid (BleUUID): BleUUID to read from

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    async def write(self, handle: BleHandle, uuid: BleUUID, data: bytearray) -> None:
        """Write a bytestream to a BleUUID.

        Args:
            handle (BleHandle): handle to pair to
            uuid (BleUUID): BleUUID to write to
            data (bytearray): bytestream to write

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    async def scan(self, token: Pattern, timeout: int = 5, service_uuids: Optional[list[BleUUID]] = None) -> BleDevice:
        """Scan BLE device with a regex in it's device name.

        Args:
            token (Pattern): Regex to scan for
            timeout (int): Time to scan (in seconds) before considering scanning as failed. Defaults to 5.
            service_uuids (list[BleUUID], Optional): The list of BleUUID's to filter on. Defaults to None.

        Returns:
            BleDevice: discovered device (shall not be multiple devices)
        """
        raise NotImplementedError

    @abstractmethod
    async def connect(self, disconnect_cb: DisconnectHandlerType, device: BleDevice, timeout: int = 15) -> BleHandle:
        """Connect to a BLE device.

        Args:
            disconnect_cb (DisconnectHandlerType): function to call when disconnect is received
            device (BleDevice): device to connect to
            timeout (int): How long to attempt connecting before giving up. Defaults to 15.

        Returns:
            BleHandle: handle that has been connected to
        """
        raise NotImplementedError

    @abstractmethod
    async def pair(self, handle: BleHandle) -> None:
        """Pair to an already connected handle.

        Args:
            handle (BleHandle): handle to pair to
        """
        raise NotImplementedError

    @abstractmethod
    async def enable_notifications(self, handle: BleHandle, handler: NotiHandlerType) -> None:
        """Enable notifications for all notifiable characteristics.

        The handler is used to register for notifications. It will be called when a a notification
        is received.

        Args:
            handle (BleHandle): handle to enable notifications on
            handler (NotiHandlerType): notification handler
        """
        raise NotImplementedError

    @abstractmethod
    async def discover_chars(self, handle: BleHandle, uuids: Optional[type[UUIDs]] = None) -> GattDB:
        """Discover all characteristics for a connected handle.

        By default, the BLE controller only knows Spec-Defined BleUUID's so any additional BleUUID's should
        be passed in with the uuids argument

        Args:
            handle (BleHandle): BLE handle to discover for
            uuids (type[UUIDs], Optional): Additional BleUUID information to use when building the
                Gatt Database. Defaults to None.

        Returns:
            GattDB: Gatt Database
        """
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self, handle: BleHandle) -> None:
        """Terminate the BLE connection.

        Args:
            handle (BleHandle): handle to disconnect from
        """
        raise NotImplementedError
