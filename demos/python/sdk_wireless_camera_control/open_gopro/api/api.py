# api.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Implementation of Open GoPro API version 2.0"""

from typing import Final

from open_gopro.interface import GoProWirelessInterface, GoProUsb, GoProHttp
from .ble_commands import BleCommands, BleSettings, BleStatuses, BleAsyncResponses
from .http_commands import HttpCommands, UsbOnlyCommands, HttpSettings


class WirelessApi:
    """Implementation of Open GoPro API version 2.0 for Wireless interface (Wifi and BLE)"""

    version: Final = "2.0"

    def __init__(self, communicator: GoProWirelessInterface) -> None:
        """Constructor

        Args:
            communicator (GoProWirelessInterface): used to communicate via BLE and Wifi
        """
        self._communicator = communicator
        self.ble_command = BleCommands(communicator)
        self.ble_setting = BleSettings(communicator)
        self.ble_status = BleStatuses(communicator)
        BleAsyncResponses.add_parsers()
        self.wifi_command = HttpCommands(communicator)
        self.wifi_setting = HttpSettings(communicator)


class UsbCommands(UsbOnlyCommands, HttpCommands):
    def __init__(self, communicator: GoProHttp):
        UsbOnlyCommands.__init__(self, communicator)
        HttpCommands.__init__(self, communicator)


class WiredApi:
    """Implementation of Open GoPro API version 2.0 for Wired interface (USB)"""

    version: Final = "2.0"

    def __init__(self, communicator: GoProUsb) -> None:
        """Constructor

        Args:
            communicator (GoProWiredInterface): used to communicate via BLE and Wifi
        """

        self._communicator = communicator
        self.http_command = UsbCommands(communicator)
        self.http_setting = HttpSettings(communicator)
