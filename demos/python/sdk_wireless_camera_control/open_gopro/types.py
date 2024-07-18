# types.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Commonly reused type aliases"""

from __future__ import annotations

from typing import Any, Callable, Coroutine, TypeAlias, Union

import construct
from google.protobuf.message import Message

from open_gopro.constants import (
    ActionId,
    BleUUID,
    CmdId,
    QueryCmdId,
    SettingId,
    StatusId,
)

# Note! We need to use Union here for Python 3.9 support

Protobuf: TypeAlias = Message

ProducerType: TypeAlias = tuple[QueryCmdId, Union[SettingId, StatusId]]
"""Types that can be registered for."""

CmdType: TypeAlias = Union[CmdId, QueryCmdId, ActionId]
"""Types that identify a command."""

ResponseType: TypeAlias = Union[CmdType, StatusId, SettingId, BleUUID, str, construct.Enum]
"""Types that are used to identify a response."""

CameraState: TypeAlias = dict[Union[SettingId, StatusId], Any]
"""Status / setting id-to-value mappings"""

JsonDict: TypeAlias = dict[str, Any]
"""Generic JSON dictionary"""

UpdateType: TypeAlias = Union[SettingId, StatusId, ActionId]
"""Identifier Type of an asynchronous update"""

UpdateCb: TypeAlias = Callable[[UpdateType, Any], Coroutine[Any, Any, None]]
"""Callback definition for update handlers"""

IdType: TypeAlias = Union[SettingId, StatusId, ActionId, CmdId, BleUUID, str]
"""Message Identifier Type"""
