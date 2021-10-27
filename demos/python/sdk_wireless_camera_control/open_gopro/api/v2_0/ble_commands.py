# ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Updates to BLE API for Open GoPro version 2.0"""

from __future__ import annotations
import logging
from typing import Type

from construct import Flag, Int8ub

from open_gopro.constants import StatusId, SettingId
from open_gopro.api.v1_0.ble_commands import BleCommandsV1_0, BleSettingsV1_0, BleStatusesV1_0
from open_gopro.communication_client import GoProBle
from open_gopro.api.builders import BleSetting, BleStatus, build_enum_adapter
from .params import ParamsV2_0 as Params

logger = logging.getLogger(__name__)


class BleCommandsV2_0(BleCommandsV1_0):
    """Version 2.0 commands are an exact copy of 1.0"""


class BleSettingsV2_0(BleSettingsV1_0):
    # pylint: disable=missing-class-docstring, unused-argument
    """Implement updates to BLE Settings for version 2.0"""

    def __init__(self, communicator: GoProBle, params: Type[Params]) -> None:
        super().__init__(communicator, params)

        class VideoPerformanceMode(BleSetting[Params.VideoPerformanceMode]):
            ...

        self.video_performance_mode = VideoPerformanceMode(
            self.communicator, SettingId.VIDEO_FOV, build_enum_adapter(params.VideoPerformanceMode)
        )
        """Video Performance Mode. Set with :py:class:`open_gopro.params.VideoPerformanceMode`"""


class BleStatusesV2_0(BleStatusesV1_0):
    """Implement updates to BLE statuses for version 2.0"""

    def __init__(self, communicator: GoProBle, params: Type[Params]) -> None:
        super().__init__(communicator, params)

        self.sd_rating_check_error: BleStatus = BleStatus(
            self.communicator, StatusId.SD_RATING_CHECK_ERROR, Flag
        )
        """Does sdcard meet specified minimum write speed?"""

        self.sd_write_speed_error: BleStatus = BleStatus(
            self.communicator, StatusId.SD_WRITE_SPEED_ERROR, Int8ub
        )
        """Number of sdcard write speed errors since device booted"""

        self.camera_control: BleStatus = BleStatus(
            self.communicator, StatusId.CAMERA_CONTROL, build_enum_adapter(params.CameraControlStatus)
        )
        """Camera control status ID"""

        self.usb_connected: BleStatus = BleStatus(self.communicator, StatusId.USB_CONNECTED, Flag)
        """Is the camera connected to a PC via USB?"""
