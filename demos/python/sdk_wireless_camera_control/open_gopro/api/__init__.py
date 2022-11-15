# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb  3 00:30:25 UTC 2022

"""Top level API module definition"""

# pylint: disable = wrong-import-position

import sys

if sys.version_info.major != 3 or not 9 <= sys.version_info.minor < 11:
    raise RuntimeError("Python >= 3.9 and < 3.11 must be used")

from .api import Api
from .ble_commands import BleCommands, BleSettings, BleStatuses
from .wifi_commands import WifiCommands, WifiSettings
from .builders import (
    BleSetting,
    BleStatus,
    BleReadCommand,
    BleAsyncResponse,
    BleProtoCommand,
    BleWriteCommand,
    RegisterUnregisterAll,
    WifiSetting,
    WifiGetBinary,
    WifiGetJsonCommand,
)
from . import params as Params
