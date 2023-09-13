# client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Open GoPro WiFi Client Implementation"""

import logging
from typing import Optional

from open_gopro.exceptions import ConnectFailed

from .controller import SsidState, WifiController

logger = logging.getLogger(__name__)


class WifiClient:
    """A Wifi client that is composed of, among other things, a Wifi interface"""

    def __init__(self, controller: WifiController) -> None:
        """Constructor

        The interface is generic and can be set with the 'controller' argument

        Args:
            controller (WifiController): controller implementation to use for this client
        """
        self._controller = controller
        self.ssid: Optional[str]
        self.password: Optional[str]

    def open(self, ssid: str, password: str, timeout: int = 15, retries: int = 5) -> None:
        """Open the WiFi client resource so that it is ready to send and receive data

        Args:
            ssid (str): [description]
            password (str): [description]
            timeout (int): [description]. Defaults to 15.
            retries (int): [description]. Defaults to 5.

        Raises:
            ConnectFailed: [description]
        """
        logger.info(f"Establishing Wifi connection to {ssid}")
        for _ in range(retries):
            if self._controller.connect(ssid, password, timeout):
                self.ssid = ssid
                self.password = password
                return
        raise ConnectFailed("Wifi failed to connect", timeout, retries)

    def close(self) -> None:
        """Close the client resource.

        This should always be called before exiting.
        """
        logger.info("Terminating the Wifi connection")
        self._controller.disconnect()

    @property
    def is_connected(self) -> bool:
        """Is the WiFi connection currently established?

        Returns:
            bool: True if yes, False if no
        """
        (ssid, state) = self._controller.current()
        return ssid is not None and state is SsidState.CONNECTED
