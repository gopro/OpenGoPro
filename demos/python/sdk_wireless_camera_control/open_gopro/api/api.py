# api.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Implementation of Open GoPro API version 2.0"""

from typing import Final

from open_gopro.interface import GoProInterface
from .ble_commands import BleCommands, BleSettings, BleStatuses, BleAsyncResponses
from .wifi_commands import WifiCommands, WifiSettings


class Api:
    """Implementation of Open GoPro API version 2.0"""

    version: Final = "2.0"

    def __init__(self, communicator: GoProInterface) -> None:
        """Constructor

        Args:
            communicator (GoProInterface): used to communicate via BLE and Wifi
        """
        self._communicator = communicator
        self.ble_command = BleCommands(communicator)
        self.ble_setting = BleSettings(communicator)
        self.ble_status = BleStatuses(communicator)
        BleAsyncResponses.add_parsers()
        self.wifi_command = WifiCommands(communicator)
        self.wifi_setting = WifiSettings(communicator)
