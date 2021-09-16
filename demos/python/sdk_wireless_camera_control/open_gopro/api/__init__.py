# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Top level API module. Used to abstract all API versions."""

from typing import Dict, Type

from open_gopro.api.v1_0.ble_commands import BleCommandsV1_0, BleSettingsV1_0, BleStatusesV1_0
from open_gopro.api.v1_0.wifi_commands import WifiSettingsV1_0, WifiCommandsV1_0
from open_gopro.api.v1_0.params import ParamsV1_0
from .v1_0.api import ApiV1_0
from .v2_0.api import ApiV2_0

# Version-agnostic type definitions
Api = ApiV1_0
BleCommands = BleCommandsV1_0
BleSettings = BleSettingsV1_0
BleStatuses = BleStatusesV1_0
WifiSettings = WifiSettingsV1_0
WifiCommands = WifiCommandsV1_0
Params = ParamsV1_0

api_versions: Dict[str, Type[Api]] = {
    api.version: api
    for api in [
        ApiV1_0,
        ApiV2_0,
    ]
}
