# controller.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""BLE Controller Interface Definition."""

import logging
from abc import ABC, abstractmethod
from typing import Callable, Generic, Pattern, TypeVar

from .services import AttributeTable

logger = logging.getLogger(__name__)

BleDevice = TypeVar("BleDevice")
BleHandle = TypeVar("BleHandle")
NotiHandlerType = Callable[[int, bytearray], None]
DisconnectHandlerType = Callable[[BleDevice], None]


class BLEController(ABC, Generic[BleDevice, BleHandle]):
    """Interface definition for a BLE driver to be used by GoPro."""

    @abstractmethod
    def read(self, handle: BleHandle, uuid: str) -> bytearray:
        """Read a bytestream response from a UUID.

        Args:
            handle (BleHandle): handle to pair to
            uuid (UUID): UUID to read from

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    def write(self, handle: BleHandle, uuid: str, data: bytearray) -> None:
        """Write a bytestream to a UUID.

        Args:
            handle (BleHandle): handle to pair to
            uuid (UUID): UUID to write to
            data (bytearray): bytestream to write

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    def scan(self, token: Pattern, timeout: int = 5) -> BleDevice:
        """Scan BLE device with a regex in it's device name.

        Args:
            token (Pattern): Regex to scan for
            timeout (int, optional): [description]. Defaults to 5.

        Returns:
            Device: discovered device (shall not be multiple devices)
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self, disconnect_cb: DisconnectHandlerType, device: BleDevice, timeout: int = 15) -> BleHandle:
        """Connect to a BLE device.

        Args:
            disconnect_cb (DisconnectHandlerType): function to call when disconnect is received
            device (BleDevice): device to connect to
            timeout (int, optional): How long to attempt connecting before giving up. Defaults to 15.

        Returns:
            handle: handle that has been connected to

        Returns:
            BleHandle: Handle to identify newly connected device
        """
        raise NotImplementedError

    @abstractmethod
    def pair(self, handle: BleHandle) -> None:
        """Pair to an already connected handle.

        Args:
            handle (BleHandle): handle to pair to
        """
        raise NotImplementedError

    @abstractmethod
    def enable_notifications(self, handle: BleHandle, handler: NotiHandlerType) -> None:
        """Enable notifications for all notifiable characteristics.

        The handler is used to register for notifications. It will be called when a a notification
        is received.

        Args:
            handle (BleHandle): handle to enable notifications on
            handler (Callable): notification handler
        """
        raise NotImplementedError

    @abstractmethod
    def discover_chars(self, handle: BleHandle) -> AttributeTable:
        """Discover all characteristics for a connected handle.

        Args:
            handle (BleHandle): handle to discover on

        Returns:
            BleHandle: handle with updated gatt_table attribute
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, handle: BleHandle) -> None:
        """Terminate the BLE connection.

        Args:
            handle (BleHandle): handle to disconnect from
        """
        raise NotImplementedError
