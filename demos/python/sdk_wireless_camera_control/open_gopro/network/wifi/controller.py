# controller.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Wifi Controller Interface Definition."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Optional

from open_gopro.domain.exceptions import InterfaceConfigFailure

logger = logging.getLogger(__name__)


class SsidState(IntEnum):
    """Current state of the SSID"""

    ESTABLISHING = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()


class WifiController(ABC):
    """Interface definition for a Wifi driver to be used by GoPro.

    Args:
        interface (str | None): Wifi interface to use. Defaults to None (auto-detect).
        password (str | None): user password to use for sudo. Defaults to None.
    """

    def __init__(self, interface: str | None = None, password: str | None = None) -> None:
        self._target_interface = interface
        self._interface: str
        self._password = password

    @abstractmethod
    async def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Connect to a network.

        Args:
            ssid (str): SSID of network to connect to
            password (str): password of network to connect to
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if successful, False otherwise
        """

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from a network.

        Returns:
            bool: True if successful, False otherwise
        """

    @abstractmethod
    def current(self) -> tuple[Optional[str], SsidState]:
        """Return the SSID and state of the current network.

        Returns:
            tuple[Optional[str], SsidState]: Tuple of SSID str and state. If SSID is None,
            there is no current connection.
        """

    @abstractmethod
    def available_interfaces(self) -> list[str]:
        """Return a list of available Wifi Interface strings

        Returns:
            list[str]: list of interfaces
        """

    @property
    def interface(self) -> str:
        """Get the Wifi Interface

        Returns:
            str: interface
        """
        return self._interface

    @interface.setter
    def interface(self, interface: Optional[str]) -> None:
        """Set the Wifi interface.

        If None is passed, interface will attempt to be auto-detected

        Args:
            interface (Optional[str]): interface (or None to auto-detect)

        Raises:
            InterfaceConfigFailure: Requested interface does not exist or not able to automatically detect
                any interfaces
        """
        detected_interfaces = self.available_interfaces()
        if interface:
            if interface in detected_interfaces:
                self._interface = interface
            else:
                raise InterfaceConfigFailure(
                    f"Requested WiFi interface [{interface}] not found among [{', '.join(detected_interfaces)}]"
                )
        else:
            if detected_interfaces:
                self._interface = detected_interfaces[0]
            else:
                raise InterfaceConfigFailure(
                    """
Can't auto-assign Wifi interface because no suitable interface was found.
Is there an available Wifi interface on this computer? To verify this, try:
    - MacOS: networksetup -listallhardwareports
    - Linux: nmcli dev
    - Windows: netsh wlan show interfaces"""
                )

    @abstractmethod
    def power(self, power: bool) -> bool:
        """Enable / disable the wireless driver.

        Args:
            power (bool): Enable if True. Disable if False.

        Returns:
            bool: was the power request successful?
        """

    @property
    @abstractmethod
    def is_on(self) -> bool:
        """Is the wireless driver currently enabled.

        Returns:
            bool: True if yes. False if no.
        """

    @property
    def sudo(self) -> str:
        """Return the sudo encapsulated password

        Returns:
            str: echo "**********" | sudo -S
        """
        if not self._password:
            return ""
        return f'echo "{self._password}" | sudo -S'
