# interfaces.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Interfaces that must be defined outside of other files to avoid circular imports."""

from abc import ABC, abstractmethod
from typing import Callable, Generic, Pattern, Optional, List, Tuple, TypeVar

from open_gopro.services import AttributeTable

NotiHandlerType = Callable[[int, bytes], None]

BleDevice = TypeVar("BleDevice")
BleClient = TypeVar("BleClient")


class BLEController(ABC, Generic[BleClient, BleDevice]):
    """Interface definition for a BLE driver to be used by GoPro."""

    @abstractmethod
    async def read(self, client: BleClient, uuid: str) -> bytearray:
        """Read a bytestream response from a UUID.

        Args:
            client (Client): client to pair to
            uuid (UUID): UUID to read from

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    async def write(self, client: BleClient, uuid: str, data: bytearray) -> None:
        """Write a bytestream to a UUID.

        Args:
            client (Client): client to pair to
            uuid (UUID): UUID to write to
            data (bytearray): bytestream to write

        Returns:
            bytearray: response
        """
        raise NotImplementedError

    @abstractmethod
    async def scan(self, token: Pattern, timeout: int = 5) -> BleDevice:
        """Scan BLE device with a regex in it's device name.

        Args:
            token (Pattern): Regex to scan for
            timeout (int, optional): [description]. Defaults to 5.

        Returns:
            Device: discovered device (shall not be multiple devices)
        """
        raise NotImplementedError

    @abstractmethod
    async def connect(self, device: BleDevice, timeout: int = 15) -> BleClient:
        """Connect to a BLE device.

        Args:
            device (Device): device to connect to
            timeout (int, optional): Timeout before considering connection establishment a failure. Defaults to 15.

        Returns:
            Client: client that has been connected to
        """
        raise NotImplementedError

    @abstractmethod
    async def pair(self, client: BleClient) -> None:
        """Pair to an already connected client.

        Args:
            client (Client): client to pair to
        """
        raise NotImplementedError

    @abstractmethod
    async def enable_notifications(self, client: BleClient, handler: NotiHandlerType) -> None:
        """Enable notifications for all notifiable characteristics.

        The handler is used to register for notifications. It will be called when a a notification
        is received.

        Args:
            client (Client): client to enable notifications on
            handler (Callable): notification handler
        """
        raise NotImplementedError

    @abstractmethod
    async def discover_chars(self, client: BleClient) -> AttributeTable:
        """Discover all characteristics for a connected client.

        Args:
            client (Client): client to discover on

        Returns:
            AttributeTable: dictionary of discovered services and characteristics indexed by UUID
        """
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self, client: BleClient) -> bool:
        """Terminate the BLE connection.

        Args:
            client (Client): client to disconnect from
        """
        raise NotImplementedError


class WifiController(ABC):
    """Interface definition for a Wifi driver to be used by GoPro."""

    @abstractmethod
    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Connect to a network.

        Args:
            ssid (str): SSID of network to connect to
            password (str): password of network to connect to
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if successful, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from a network.

        Returns:
            bool: True if successful, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """Return the SSID and state of the current network.

        Returns:
            Tuple[Optional[str], Optional[str]]: Tuple of SSID and state. State is optional. If SSID is None,
            there is no current connection
        """
        raise NotImplementedError

    @abstractmethod
    def interfaces(self) -> List[str]:
        """Return a list of wireless adapters.

        Returns:
            List[str]: adapters
        """
        raise NotImplementedError

    @abstractmethod
    def interface(self, interface: Optional[str]) -> Optional[str]:
        """Get or set the currently used wireless adapter.

        Args:
            interface (str, optional): Get if the interface parameter is None. Set otherwise. Defaults to None.

        Returns:
            Optional[str]: Name of interface if get. None if set.
        """
        raise NotImplementedError

    @abstractmethod
    def power(self, power: bool) -> None:
        """Enable / disable the wireless driver.

        Args:
            power (bool, optional): Enable if True. Disable if False.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_on(self) -> bool:
        """Is the wireless driver currently enabled.

        Returns:
            bool: True if yes. False if no.
        """
        raise NotImplementedError


class GoProError(Exception):
    """Base class for other exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(f"GoPro Error: {message}")


class ScanFailedToFindDevice(GoProError):
    """The scan failed without finding a device."""

    def __init__(self) -> None:
        super().__init__("A scan timed out without finding a device")


class ConnectFailed(GoProError):
    """A BLE or WiFi connection failed to establish

    Args:
        connection (str): type of connection that failed
        retries (int): how many retries were attempted
        timeout (int): the timeout used for each attempt
    """

    def __init__(self, connection: str, timeout: float, retries: int):
        super().__init__(
            f"{connection} connection failed to establish after {retries} retries with timeout {timeout}"
        )


class ResponseTimeout(GoProError):
    """A response has timed out."""

    def __init__(self, timeout: float) -> None:
        super().__init__(f"Response timeout occurred of {timeout} seconds")


class GoProNotInitialized(GoProError):
    """A command was attempted without waiting for the GoPro instance to initialize."""

    def __init__(self) -> None:
        super().__init__("GoPro has not been initialized yet")
