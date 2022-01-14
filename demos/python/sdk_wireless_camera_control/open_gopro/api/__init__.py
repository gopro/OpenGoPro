# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Top level API module. Used to abstract all API versions."""

from typing import Dict, Type, Union

from open_gopro.api.v1_0.ble_commands import BleCommandsV1_0, BleSettingsV1_0, BleStatusesV1_0
from open_gopro.api.v1_0.wifi_commands import WifiSettingsV1_0, WifiCommandsV1_0
from open_gopro.api.v1_0.params import ParamsV1_0
from open_gopro.api.v2_0.ble_commands import BleCommandsV2_0, BleSettingsV2_0, BleStatusesV2_0
from open_gopro.api.v2_0.wifi_commands import WifiSettingsV2_0, WifiCommandsV2_0
from open_gopro.api.v2_0.params import ParamsV2_0
from .v1_0.api import ApiV1_0
from .v2_0.api import ApiV2_0

# Version-agnostic type definitions
Api = Union[ApiV1_0, ApiV2_0]
BleCommands = Union[BleCommandsV1_0, BleCommandsV2_0]
BleSettings = Union[BleSettingsV1_0, BleSettingsV2_0]
BleStatuses = Union[BleStatusesV1_0, BleStatusesV2_0]
WifiSettings = Union[WifiSettingsV1_0, WifiSettingsV2_0]
WifiCommands = Union[WifiCommandsV1_0, WifiCommandsV2_0]
Params = Union[ParamsV1_0, ParamsV2_0]

api_versions: Dict[str, Type[Api]] = {
    api.version: api
    for api in [
        ApiV1_0,
        ApiV2_0,
    ]
}
