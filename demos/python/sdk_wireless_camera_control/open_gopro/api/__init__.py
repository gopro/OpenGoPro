# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb  3 00:30:25 UTC 2022

"""Top level API module definition"""

from . import params as Params
from .api import WiredApi, WirelessApi
from .ble_commands import BleCommands, BleSettings, BleStatuses
from .builders import (
    BleAsyncResponse,
    BleProtoCommand,
    BleReadCommand,
    BleSetting,
    BleStatus,
    BleWriteCommand,
    HttpGetBinary,
    HttpGetJsonCommand,
    HttpSetting,
    RegisterUnregisterAll,
)
from .http_commands import HttpCommands, HttpSettings

# TODO find a better way to set up parsers, etc besides instantiating

WirelessApi(None)  # type: ignore
