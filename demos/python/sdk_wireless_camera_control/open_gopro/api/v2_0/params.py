# params.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

# pylint: disable=missing-class-docstring

"""Updates to parameter definitions for GoPro BLE and WiFi commands for Open GoPro version 2.0"""

from open_gopro.constants import GoProEnum
from open_gopro.api.v1_0.params import ParamsV1_0


class ParamsV2_0(ParamsV1_0):
    class Resolution(GoProEnum):
        NOT_APPLICABLE = 0
        RES_4K = 1
        RES_2_7K = 4
        RES_2_7K_4_3 = 6
        RES_1080 = 9
        RES_4K_4_3 = 18
        RES_5_K_4_3 = 25
        RES_5_3_K = 100

    class Preset(GoProEnum):
        STANDARD = 0x00000000
        ACTIVITY = 0x00000001
        CINEMATIC = 0x00000002
        ULTRA_SLOMO = 0x00000004
        BASIC = 0x00000005
        PHOTO = 0x00010000
        LIVE_BURST = 0x00010001
        BURST_PHOTO = 0x00010002
        NIGHT_PHOTO = 0x00010003
        TIME_WARP = 0x00020000
        TIME_LAPSE = 0x00020001
        NIGHT_LAPSE = 0x00020002
        STANDARD_EB = 0x00080000
        ACTIVITY_EB = 0x00080001
        CINEMATIC_EB = 0x00080002
        SLOMO_EB = 0x00080003
        TRIPOD_4K = 0x00090000
        TRIPOD_5_3K = 0x00090001

    class LED(GoProEnum):
        ALL_ON = 3
        ALL_OFF = 4
        FRONT_OFF_ONLY = 5
        BLE_KEEP_ALIVE = 66

    class CameraControlStatus(GoProEnum):
        IDLE = 0
        CAMERA = 1
        EXTERNAL = 2

    class VideoFOV(GoProEnum):
        WIDE = 0
        NARROW = 2
        SUPERVIEW = 3
        LINEAR = 4
        MAX_SUPERVIEW = 7
        LINEAR_HORIZON = 8

    class PhotoFOV(GoProEnum):
        NOT_APPLICABLE = 0
        WIDE = 101
        LINEAR = 102
        NARROW = 19
        MAX_SUPERVIEW = 100

    class MultishotFOV(GoProEnum):
        NOT_APPLICABLE = 0
        NARROW = 19
        MAX_SUPERVIEW = 100
        WIDE = 101

    class VideoPerformanceMode(GoProEnum):
        MAX_PERFORMANCE = 0
        EXTENDED_BATTERY = 1
        STATIONARY = 2
