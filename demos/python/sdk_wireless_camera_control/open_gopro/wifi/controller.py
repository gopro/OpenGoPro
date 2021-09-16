# controller.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Wifi Controller Interface Definition."""

import logging
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)


class SsidState(IntEnum):
    """Current state of the SSID"""

    ESTABLISHING = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()


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
    def current(self) -> Tuple[Optional[str], SsidState]:
        """Return the SSID and state of the current network.

        Returns:
            Tuple[Optional[str], SsidState]: Tuple of SSID str and state. If SSID is None,
            there is no current connection.
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
    def power(self, power: bool) -> bool:
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
