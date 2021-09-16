# api.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Implementation of Open GoPro API version 1.0"""

from open_gopro.communication_client import GoProBle, GoProWifi
from .ble_commands import BleCommandsV1_0, BleSettingsV1_0, BleStatusesV1_0
from .wifi_commands import WifiCommandsV1_0, WifiSettingsV1_0
from .params import ParamsV1_0


class ApiV1_0:
    """Implementation of Open GoPro API version 1.0"""

    version = "1.0"

    def __init__(self, ble_communicator: GoProBle, wifi_communicator: GoProWifi) -> None:
        self.params = ParamsV1_0
        self.ble_command = BleCommandsV1_0(ble_communicator)
        self.ble_setting = BleSettingsV1_0(ble_communicator, self.params)
        self.ble_status = BleStatusesV1_0(ble_communicator, self.params)
        self.wifi_command = WifiCommandsV1_0(wifi_communicator)
        self.wifi_setting = WifiSettingsV1_0(wifi_communicator, self.params)
