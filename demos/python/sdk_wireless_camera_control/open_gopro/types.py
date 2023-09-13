# types.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Commonly reused type aliases"""

from __future__ import annotations

from typing import Any, Callable, Coroutine, Union

import construct
from google.protobuf.message import Message as Protobuf  # pylint: disable=unused-import

from open_gopro.constants import (
    ActionId,
    BleUUID,
    CmdId,
    QueryCmdId,
    SettingId,
    StatusId,
)

# Note! We need to use Union here for Python 3.9 support

ProducerType = tuple[QueryCmdId, Union[SettingId, StatusId]]
"""Types that can be registered for."""

CmdType = Union[CmdId, QueryCmdId, ActionId]
"""Types that identify a command."""

ResponseType = Union[CmdType, StatusId, SettingId, BleUUID, str, construct.Enum]
"""Types that are used to identify a response."""

CameraState = dict[Union[SettingId, StatusId], Any]

JsonDict = dict[str, Any]

UpdateType = Union[SettingId, StatusId, ActionId]
UpdateCb = Callable[[UpdateType, Any], Coroutine[Any, Any, None]]
