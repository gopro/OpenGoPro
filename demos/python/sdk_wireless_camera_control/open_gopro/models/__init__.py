# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jun 26 18:26:05 UTC 2023

"""Data models for use throughout this package"""

from .general import (
    CameraInfo,
    CohnInfo,
    HttpInvalidSettingResponse,
    ScheduledCapture,
    TzDstDateTime,
)
from .media_list import (
    GroupedMediaItem,
    MediaItem,
    MediaList,
    MediaMetadata,
    MediaPath,
    PhotoMetadata,
    VideoMetadata,
)
from .network_scan_responses import AdvData, DnsScanResponse, GoProAdvData
from .response import GoProBlePacketHeader, GoProResp
