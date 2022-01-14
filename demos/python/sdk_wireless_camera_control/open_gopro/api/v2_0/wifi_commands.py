# wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Updates to WiFi API for Open GoPro version 2.0"""

from __future__ import annotations
import logging
from typing import Type

from open_gopro.communication_client import GoProWifi
from open_gopro.api.v1_0.wifi_commands import WifiCommandsV1_0, WifiSettingsV1_0
from open_gopro.api.v2_0.params import ParamsV2_0 as Params
from open_gopro.api.builders import WifiGetJsonNoParams, WifiGetJsonWithParams, WifiSetting
from open_gopro.constants import SettingId

logger = logging.getLogger(__name__)


class WifiCommandsV2_0(WifiCommandsV1_0):
    """All of the Wifi commands.

    To be used as a delegate for a GoProWifi to build commands

    All of these return a GoProResp

    Args:
        communicator (GoProWifi): [description]
    """

    def __init__(self, communicator: GoProWifi):
        super().__init__(communicator)

        self.set_third_party_client_info = WifiGetJsonNoParams(
            communicator, "/gopro/camera/analytics/set_client_info"
        )
        """Flag as third party app.

        Will return error if the camera is already encoding.

        Returns:
            GoProResp: command status
        """

        self.set_shutter_on = WifiGetJsonNoParams(communicator, "/gopro/camera/shutter/start")
        """Set the shutter on (i.e. start encoding).

        Returns:
            GoProResp: command status
        """

        self.set_shutter_off = WifiGetJsonNoParams(communicator, "/gopro/camera/shutter/stop")
        """Set the shutter off (i.e. stop encoding).

        Will return error tf this command is sent when the camera is not encoding.

        Returns:
            GoProResp: command status
        """

        self.set_camera_control = WifiGetJsonWithParams[Params.CameraControl](
            communicator, "/gopro/camera/control/set_ui_controller?p={}"
        )
        """Configure global behaviors by setting camera control (to i.e. Idle, External)

        Args:
            value (Params.CameraControl): desired camera control value

        Returns:
            GoProResp: command status
        """


class WifiSettingsV2_0(WifiSettingsV1_0):
    """Updates to WiFi settings for Open GoPro version 2.0"""

    def __init__(self, communicator: GoProWifi, params: Type[Params]):
        super().__init__(communicator, params, endpoint="gopro/camera/setting?setting={}&option={}")

        self.video_performance_mode = WifiSetting[Params.VideoPerformanceMode](
            communicator, SettingId.VIDEO_PERFORMANCE_MODE
        )
        """Video Performance Mode (extended battery, tripod, etc)."""
