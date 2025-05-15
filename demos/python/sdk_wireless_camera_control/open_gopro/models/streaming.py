# streaming.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu May 15 16:57:28 UTC 2025

"""Streaming models and entities."""

import enum
from dataclasses import dataclass
from pathlib import Path

from pydantic import Field

from open_gopro.domain.enum import GoProEnum, GoProIntEnum
from open_gopro.models.bases import CustomBaseModel
from open_gopro.models.general import SupportedOption
from open_gopro.models.proto import EnumLens, EnumWindowSize


class StreamType(enum.Enum):
    """Enum for the different types of streams."""

    WEBCAM = enum.auto()
    LIVE = enum.auto()
    PREVIEW = enum.auto()


class WebcamResolution(GoProIntEnum):
    """Possible Webcam Resolutions"""

    NOT_APPLICABLE = 0
    RES_480 = 4
    RES_720 = 7
    RES_1080 = 12


class WebcamFOV(GoProIntEnum):
    """Possible Webcam FOVs"""

    WIDE = 0
    NARROW = 2
    SUPERVIEW = 3
    LINEAR = 4


class WebcamProtocol(GoProEnum):
    """Possible Webcam Protocols"""

    TS = "TS"
    RTSP = "RTSP"


class WebcamStatus(GoProIntEnum):
    """Webcam Statuses / states"""

    OFF = 0
    IDLE = 1
    HIGH_POWER_PREVIEW = 2
    LOW_POWER_PREVIEW = 3


class WebcamError(GoProIntEnum):
    """Errors common among Webcam commands"""

    SUCCESS = 0
    SET_PRESET = 1
    SET_WINDOW_SIZE = 2
    EXEC_STREAM = 3
    SHUTTER = 4
    COM_TIMEOUT = 5
    INVALID_PARAM = 6
    UNAVAILABLE = 7
    EXIT = 8


class WebcamResponse(CustomBaseModel):
    """Common Response from Webcam Commands"""

    status: WebcamStatus | None = Field(default=None)
    error: WebcamError
    setting_id: str | None = Field(default=None)
    supported_options: list[SupportedOption] | None = Field(default=None)


@dataclass
class LivestreamOptions:
    """Livestream-specific stream setup options"""

    url: str
    minimum_bitrate: int = 1000
    maximum_bitrate: int = 1000
    starting_bitrate: int = 1000
    encode: bool = True
    resolution: EnumWindowSize.ValueType | None = None
    fov: EnumLens.ValueType | None = None
    certs: list[Path] | None = None


@dataclass
class PreviewStreamOptions:
    """Preview stream-specific stream setup options"""

    port: int | None = None


@dataclass
class WebcamStreamOptions:
    """Webcam stream-specific stream setup options"""

    resolution: WebcamResolution | None = None
    protocol: WebcamProtocol | None = None
    fov: WebcamFOV | None = None
    port: int | None = None
