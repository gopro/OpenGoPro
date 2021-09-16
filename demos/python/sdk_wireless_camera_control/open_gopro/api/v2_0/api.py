# api.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Implementation of Open GoPro API version 2.0"""

from open_gopro.api.v1_0.api import ApiV1_0
from open_gopro.communication_client import GoProBle, GoProWifi
from .ble_commands import BleCommandsV2_0, BleSettingsV2_0, BleStatusesV2_0
from .wifi_commands import WifiCommandsV2_0, WifiSettingsV2_0
from .params import ParamsV2_0


class ApiV2_0(ApiV1_0):
    """Implementation of Open GoPro API version 2.0"""

    version = "2.0"

    def __init__(  # pylint: disable = super-init-not-called
        self, ble_communicator: GoProBle, wifi_communicator: GoProWifi
    ) -> None:  # pylint: disable = super-init-not-called
        # No call to superclass's __init__ since we are overriding each individual attribute below. Would be redundant.
        self.params = ParamsV2_0
        self.ble_command = BleCommandsV2_0(ble_communicator)
        self.ble_setting = BleSettingsV2_0(ble_communicator, self.params)
        self.ble_status = BleStatusesV2_0(ble_communicator, self.params)
        self.wifi_command = WifiCommandsV2_0(wifi_communicator)
        self.wifi_setting = WifiSettingsV2_0(wifi_communicator, self.params)
