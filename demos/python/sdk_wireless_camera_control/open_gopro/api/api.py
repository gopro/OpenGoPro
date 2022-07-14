# api.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Implementation of Open GoPro API version 2.0"""

from typing import Final

from open_gopro.communication_client import GoProBle, GoProWifi
from .ble_commands import BleCommands, BleSettings, BleStatuses, BleAsyncResponses
from .wifi_commands import WifiCommands, WifiSettings


class Api:
    """Implementation of Open GoPro API version 2.0"""

    version: Final = "2.0"

    def __init__(self, ble_communicator: GoProBle, wifi_communicator: GoProWifi) -> None:
        """Constructor

        Args:
            ble_communicator (GoProBle): used to communicate via BLE
            wifi_communicator (GoProWifi): used to communicate via WiFi
        """
        self.ble_command = BleCommands(ble_communicator)
        self.ble_setting = BleSettings(ble_communicator)
        self.ble_status = BleStatuses(ble_communicator)
        BleAsyncResponses.add_parsers(ble_communicator)
        self.wifi_command = WifiCommands(wifi_communicator)
        self.wifi_setting = WifiSettings(wifi_communicator)
