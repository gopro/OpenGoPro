# types.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Commonly reused type aliases"""

from __future__ import annotations

from typing import Any, Callable, Coroutine, TypeAlias

import construct
from google.protobuf.message import Message

from open_gopro.models.constants import ActionId, CmdId, QueryCmdId, SettingId, StatusId
from open_gopro.models.streaming import (
    LivestreamOptions,
    PreviewStreamOptions,
    WebcamStreamOptions,
)
from open_gopro.network.ble.services import BleUUID

Protobuf: TypeAlias = Message

ProducerType: TypeAlias = tuple[QueryCmdId, SettingId | StatusId]
"""Types that can be registered for."""

CmdType: TypeAlias = CmdId | QueryCmdId | ActionId
"""Types that identify a command."""

ResponseType: TypeAlias = CmdType | StatusId | SettingId | BleUUID | str | construct.Enum
"""Types that are used to identify a response."""

CameraState: TypeAlias = dict[SettingId | StatusId, Any]
"""Status / setting id-to-value mappings"""

JsonDict: TypeAlias = dict[str, Any]
"""Generic JSON dictionary"""

UpdateType: TypeAlias = SettingId | StatusId | ActionId
"""Identifier Type of an asynchronous update"""

UpdateCb: TypeAlias = Callable[[UpdateType, Any], Coroutine[Any, Any, None]]
"""Callback definition for update handlers"""

IdType: TypeAlias = SettingId | StatusId | ActionId | CmdId | BleUUID | str
"""Message Identifier Type"""

StreamOptions: TypeAlias = WebcamStreamOptions | LivestreamOptions | PreviewStreamOptions
"""Union of all stream option types"""
