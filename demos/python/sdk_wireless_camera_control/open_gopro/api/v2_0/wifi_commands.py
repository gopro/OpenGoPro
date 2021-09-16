# wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Updates to WiFi API for Open GoPro version 2.0"""

from __future__ import annotations
import logging
from typing import Type, TYPE_CHECKING

# from open_gopro import GoProResp
from open_gopro.communication_client import GoProWifi
from open_gopro.api.v1_0.wifi_commands import WifiCommandsV1_0, WifiSettingsV1_0
from open_gopro.api.builders import WifiGetJsonNoParams

if TYPE_CHECKING:
    from .params import ParamsV2_0 as Params

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
        """Flag as third party app."""

        self.set_shutter_on = WifiGetJsonNoParams(communicator, "/gopro/camera/shutter/start")
        """Set the shutter on (i.e. start encoding)."""

        self.set_shutter_off = WifiGetJsonNoParams(communicator, "/gopro/camera/shutter/stop")
        """Set the shutter off (i.e. stop encoding)."""


class WifiSettingsV2_0(WifiSettingsV1_0):
    """Updates to WiFi settings for Open GoPro version 2.0"""

    def __init__(self, communicator: GoProWifi, params: Type[Params]):
        super().__init__(communicator, params, endpoint="gopro/camera/setting?setting={}&option={}")
