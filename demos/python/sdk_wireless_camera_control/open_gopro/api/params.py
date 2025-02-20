# params.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep  6 19:25:51 UTC 2024

# pylint: disable=missing-class-docstring, no-member

"""Parameter definitions for GoPro BLE and WiFi commands for Open GoPro version 2_0"""

from __future__ import annotations

from open_gopro.enum import GoProEnum, GoProIntEnum


class Toggle(GoProIntEnum):
    ENABLE = 1
    DISABLE = 0


class AnalyticsState(GoProIntEnum):
    NOT_READY = 0
    READY = 1
    ON_CONNECT = 2


class MaxLensMode(GoProIntEnum):
    DEFAULT = 0
    MAX_LENS = 1


class ExposureMode(GoProIntEnum):
    DISABLED = 0
    AUTO = 1
    ISO_LOCK = 2
    HEMISPHERE = 3


class WifiBand(GoProIntEnum):
    BAND_2_4_GHZ = 0
    BAND_5_GHZ = 1
    BAND_MAX = 2


class Flatmode(GoProIntEnum):
    NOT_APPLICABLE = 0
    VIDEO = 12
    LOOPING = 15
    SINGLE_PHOTO = 16
    NIGHT_PHOTO = 18
    BURST_PHOTO = 19
    TIME_LAPSE_VIDEO = 13
    TIME_LAPSE_PHOTO = 20
    NIGHT_LAPSE_PHOTO = 21
    WEBCAM = 23
    TIME_WARP_VIDEO = 24
    LIVE_BURST = 25
    NIGHT_LAPSE_VIDEO = 26
    SLO_MO = 27
    UNKNOWN = 28


class MediaModStatus(GoProIntEnum):
    SELFIE_0_HDMI_0_MEDIAMODCONNECTED_FALSE = 0
    SELFIE_0_HDMI_0_MEDIAMODCONNECTED_TRUE = 1
    SELFIE_0_HDMI_1_MEDIAMODCONNECTED_FALSE = 2
    SELFIE_0_HDMI_1_MEDIAMODCONNECTED_TRUE = 3
    SELFIE_1_HDMI_0_MEDIAMODCONNECTED_FALSE = 4
    SELFIE_1_HDMI_0_MEDIAMODCONNECTED_TRUE = 5
    SELFIE_1_HDMI_1_MEDIAMODCONNECTED_FALSE = 6
    SELFIE_1_HDMI_1_MEDIAMODCONNECTED_TRUE = 7


class LensModStatus(GoProIntEnum):
    INVALID = -1
    DEFAULT = 0
    MAX_LENS = 1
    MAX_LENS_2_0 = 2
    MAX_LENS_2_5 = 3
    MACRO = 4
    ANAMORPHIC = 5
    ND_4 = 6
    ND_8 = 7
    ND_16 = 8
    ND_32 = 9
    NONE = 10


class LED(GoProIntEnum):
    BLE_KEEP_ALIVE = 66


class Orientation(GoProIntEnum):
    UPRIGHT = 0
    UPSIDE_DOWN = 1
    ON_RIGHT_SIDE = 2
    ON_LEFT_SIDE = 3


class MediaModMicStatus(GoProIntEnum):
    REMOVED = 0
    ONLY = 1
    WITH_EXTERNAL = 2


class TimeWarpSpeed(GoProIntEnum):
    SPEED_15X = 0
    SPEED_30X = 1
    SPEED_60X = 2
    SPEED_150X = 3
    SPEED_300X = 4
    SPEED_900X = 5
    SPEED_1800X = 6
    SPEED_2X = 7
    SPEED_5X = 8
    SPEED_10X = 9
    SPEED_AUTO = 10
    SPEED_1X = 11
    SPEED_HALF = 12


class CameraControl(GoProIntEnum):
    IDLE = 0
    CAMERA = 1
    EXTERNAL = 2


class WebcamResolution(GoProIntEnum):
    NOT_APPLICABLE = 0
    RES_480 = 4
    RES_720 = 7
    RES_1080 = 12


class WebcamFOV(GoProIntEnum):
    WIDE = 0
    NARROW = 2
    SUPERVIEW = 3
    LINEAR = 4


class WebcamProtocol(GoProEnum):
    TS = "TS"
    RTSP = "RTSP"


class PairState(GoProIntEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FAILED = 2
    STOPPED = 3
    COMPLETED = 4


class PairType(GoProIntEnum):
    NOT_PAIRING = 0
    PAIRING_APP = 1
    PAIRING_REMOTE_CONTROL = 2
    PAIRING_BLUETOOTH = 3


class WAPState(GoProIntEnum):
    NEVER_STARTED = 0
    STARTED = 1
    ABORTED = 2
    CANCELED = 3
    COMPLETED = 4


class SDStatus(GoProIntEnum):
    OK = 0
    FULL = 1
    REMOVED = 2
    FORMAT_ERROR = 3
    BUSY = 4
    SWAPPED = 8
    UNKNOWN = 0xFF


class OTAStatus(GoProIntEnum):
    IDLE = 0
    DOWNLOADING = 1
    VERIFYING = 2
    DOWNLOAD_FAILED = 3
    VERIFY_FAILED = 4
    READY = 5
    GOPRO_APP_DOWNLOADING = 6
    GOPRO_APP_VERIFYING = 7
    GOPRO_APP_DOWNLOAD_FAILED = 8
    GOPRO_APP_VERIFY_FAILED = 9
    GOPRO_APP_READY = 10
