# params.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=missing-class-docstring, no-member

"""Parameter definitions for GoPro BLE and WiFi commands for Open GoPro version 2.0"""

from __future__ import annotations

from open_gopro.constants import GoProEnum


class Resolution(GoProEnum):
    NOT_APPLICABLE = 0
    RES_4K = 1
    RES_2_7K = 4
    RES_2_7K_4_3 = 6
    RES_1440 = 7
    RES_1080 = 9
    RES_4K_4_3 = 18
    RES_5K = 24
    RES_5K_4_3 = 25
    RES_5_3K_8_7 = 26
    RES_5_3K_4_3 = 27
    RES_4K_8_7 = 28
    RES_4K_9_16 = 29
    RES_1080_9_16 = 30
    RES_5_3K = 100
    RES_5_3K_16_9 = 101
    RES_4K_16_9 = 102
    RES_4K_4_3_TODO = 103
    RES_2_7K_16_9 = 104
    RES_2_7K_4_3_TODO = 105
    RES_1080_16_9 = 106


class WebcamResolution(GoProEnum):
    NOT_APPLICABLE = 0
    RES_480 = 4
    RES_720 = 7
    RES_1080 = 12


class FPS(GoProEnum):
    FPS_240 = 0
    FPS_120 = 1
    FPS_100 = 2
    FPS_60 = 5
    FPS_50 = 6
    FPS_30 = 8
    FPS_25 = 9
    FPS_24 = 10
    FPS_200 = 13


class AutoOff(GoProEnum):
    NEVER = 0
    MIN_1 = 1
    MIN_5 = 4
    MIN_15 = 6
    MIN_30 = 7
    SEC_8 = 11
    SEC_30 = 12


class LensMode(GoProEnum):
    SINGLE = 0
    DUAL = 5


class VideoFOV(GoProEnum):
    WIDE = 0
    NARROW = 2
    SUPERVIEW = 3
    LINEAR = 4
    MAX_SUPERVIEW = 7
    LINEAR_HORIZON_LEVELING = 8
    HYPERVIEW = 9
    LINEAR_HORIZON_LOCK = 10
    MAX_HYPERVIEW = 11


class WebcamFOV(GoProEnum):
    WIDE = 0
    NARROW = 2
    SUPERVIEW = 3
    LINEAR = 4


class PhotoFOV(GoProEnum):
    NOT_APPLICABLE = 0
    HYPERVIEW = 9
    NARROW = 19
    WIDE = 101
    LINEAR = 102
    MAX_SUPERVIEW = 100
    LINEAR_HORIZON = 121


class MultishotFOV(GoProEnum):
    NOT_APPLICABLE = 0
    NARROW = 19
    MAX_SUPERVIEW = 100
    WIDE = 101
    LINEAR = 102


class LED(GoProEnum):
    LED_2 = 2
    ALL_ON = 3
    ALL_OFF = 4
    FRONT_OFF_ONLY = 5
    BLE_KEEP_ALIVE = 66


class PairState(GoProEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FAILED = 2
    STOPPED = 3
    COMPLETED = 4


class PairType(GoProEnum):
    NOT_PAIRING = 0
    PAIRING_APP = 1
    PAIRING_REMOTE_CONTROL = 2
    PAIRING_BLUETOOTH = 3


class WAPState(GoProEnum):
    NEVER_STARTED = 0
    STARTED = 1
    ABORTED = 2
    CANCELED = 3
    COMPLETED = 4


class SDStatus(GoProEnum):
    OK = 0
    FULL = 1
    REMOVED = 2
    FORMAT_ERROR = 3
    BUSY = 4
    SWAPPED = 8
    UNKNOWN = 0xFF


class OTAStatus(GoProEnum):
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


class AnalyticsState(GoProEnum):
    NOT_READY = 0
    READY = 1
    ON_CONNECT = 2


class ExposureMode(GoProEnum):
    DISABLED = 0
    AUTO = 1
    ISO_LOCK = 2
    HEMISPHERE = 3


class AccMicStatus(GoProEnum):
    NOT_CONNECTED = 0
    CONNECTED = 1
    CONNECTED_AND_PLUGGED_IN = 2


class WifiBand(GoProEnum):
    BAND_2_4_GHZ = 0
    BAND_5_GHZ = 1
    BAND_MAX = 2


class Orientation(GoProEnum):
    UPRIGHT = 0
    UPSIDE_DOWN = 1
    ON_RIGHT_SIDE = 2
    ON_LEFT_SIDE = 3


class MediaModMicStatus(GoProEnum):
    REMOVED = 0
    ONLY = 1
    WITH_EXTERNAL = 2


class TimeWarpSpeed(GoProEnum):
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


class MaxLensMode(GoProEnum):
    DEFAULT = 0
    MAX_LENS = 1


class MediaModStatus(GoProEnum):
    SELFIE_0_HDMI_0_MEDIAMODCONNECTED_FALSE = 0
    SELFIE_0_HDMI_0_MEDIAMODCONNECTED_TRUE = 1
    SELFIE_0_HDMI_1_MEDIAMODCONNECTED_FALSE = 2
    SELFIE_0_HDMI_1_MEDIAMODCONNECTED_TRUE = 3
    SELFIE_1_HDMI_0_MEDIAMODCONNECTED_FALSE = 4
    SELFIE_1_HDMI_0_MEDIAMODCONNECTED_TRUE = 5
    SELFIE_1_HDMI_1_MEDIAMODCONNECTED_FALSE = 6
    SELFIE_1_HDMI_1_MEDIAMODCONNECTED_TRUE = 7


class Flatmode(GoProEnum):
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


class Toggle(GoProEnum):
    ENABLE = 1
    DISABLE = 0


class HypersmoothMode(GoProEnum):
    OFF = 0
    ON = 1
    HIGH = 2
    BOOST = 3
    AUTO_BOOST = 4
    STANDARD = 100


class CameraControl(GoProEnum):
    IDLE = 0
    CAMERA = 1
    EXTERNAL = 2


class PerformanceMode(GoProEnum):
    MAX_PERFORMANCE = 0
    EXTENDED_BATTERY = 1
    STATIONARY = 2


class MediaFormat(GoProEnum):
    TIME_LAPSE_VIDEO = 13
    TIME_LAPSE_PHOTO = 20
    NIGHT_LAPSE_PHOTO = 21
    NIGHT_LAPSE_VIDEO = 26


class AntiFlicker(GoProEnum):
    HZ_60 = 2
    HZ_50 = 3


class CameraUxMode(GoProEnum):
    EASY = 0
    PRO = 1


class HorizonLeveling(GoProEnum):
    OFF = 0
    ON = 1
    LOCKED = 2


class Speed(GoProEnum):
    ULTRA_SLO_MO_8X = 0
    SUPER_SLO_MO_4X = 1
    SLO_MO_2X = 2
    LOW_LIGHT_1X = 3
    SUPER_SLO_MO_4X_EXT_BATT = 4
    SLO_MO_2X_EXT_BATT = 5
    LOW_LIGHT_1X_EXT_BATT = 6
    ULTRA_SLO_MO_8X_50_HZ = 7
    SUPER_SLO_MO_4X_50_HZ = 8
    SLO_MO_2X_50_HZ = 9
    LOW_LIGHT_1X_50_HZ = 10
    SUPER_SLO_MO_4X_EXT_BATT_50_HZ = 11
    SLO_MO_2X_EXT_BATT_50_HZ = 12
    LOW_LIGHT_1X_EXT_BATT_50_HZ = 13
    ULTRA_SLO_MO_8X_EXT_BATT = 14
    ULTRA_SLO_MO_8X_EXT_BATT_50_HZ = 15
    ULTRA_SLO_MO_8X_LONG_BATT = 16
    SUPER_SLO_MO_4X_LONG_BATT = 17
    SLO_MO_2X_LONG_BATT = 18
    LOW_LIGHT_1X_LONG_BATT = 19
    ULTRA_SLO_MO_8X_LONG_BATT_50_HZ = 20
    SUPER_SLO_MO_4X_LONG_BATT_50_HZ = 21
    SLO_MO_2X_LONG_BATT_50_HZ = 22
    LOW_LIGHT_1X_LONG_BATT_50_HZ = 23
    SLO_MO_2X_4K = 24
    SUPER_SLO_MO_4X_2_7_K = 25
    SLO_MO_2X_4K_50_HZ = 26
    SUPER_SLO_MO_4X_2_7_K_50_HZ = 27
    SUPER_SLO_MO_4X_2_7K_50HZ = 27
    SPEED_1X_LOW_LIGHT = 28
    SPEED_1X_LOW_LIGHT_2 = 29
    SLO_MO_2X_2 = 30
    SLO_MO_2X_3 = 31
    SPEED_1X_LOW_LIGHT_3 = 32
    SPEED_1X_LOW_LIGHT_4 = 33
    SLO_MO_2X_4 = 34
    SLO_MO_2X_5 = 35
    SPEED_1X_LOW_LIGHT_5 = 36
    SPEED_1X_LOW_LIGHT_6 = 37
    SPEED_1X_LOW_LIGHT_7 = 38
    SPEED_1X_LOW_LIGHT_8 = 39
    SLO_MO_2X_6 = 40
    SLO_MO_2X_7 = 41
    SLO_MO_2X_8 = 42
    SLO_MO_2X_9 = 43
    SPEED_1X_LOW_LIGHT_9 = 44
    SPEED_1X_LOW_LIGHT_10 = 45
    SPEED_1X_LOW_LIGHT_11 = 46
    SPEED_1X_LOW_LIGHT_12 = 47


class PhotoEasyMode(GoProEnum):
    OFF = 0
    ON = 1
    SUPER_PHOTO = 100
    NIGHT_PHOTO = 101


class StarTrailLength(GoProEnum):
    NOT_APPLICABLE = 0
    SHORT = 1
    LONG = 2
    MAX = 3


class SystemVideoMode(GoProEnum):
    HIGHEST_QUALITY = 0
    EXTENDED_BATTERY = 1
    EXTENDED_BATTERY_GREEN_ICON = 101
    LONGEST_BATTERY_GREEN_ICON = 102


class BitRate(GoProEnum):
    STANDARD = 0
    HIGH = 1


class BitDepth(GoProEnum):
    BIT_8 = 0
    BIT_10 = 2


class VideoProfile(GoProEnum):
    STANDARD = 0
    HDR = 1
    LOG = 2


class VideoAspectRatio(GoProEnum):
    RATIO_4_3 = 0
    RATIO_16_9 = 1
    RATIO_8_7 = 3
    RATIO_9_16 = 4


class EasyAspectRatio(GoProEnum):
    WIDESCREEN = 0
    MOBILE = 1
    UNIVERSAL = 2


class VideoMode(GoProEnum):
    HIGHEST = 0
    STANDARD = 1
    BASIC = 2


class TimelapseMode(GoProEnum):
    TIMEWARP = 0
    STAR_TRAILS = 1
    LIGHT_PAINTING = 2
    VEHICLE_LIGHTS = 3
    MAX_TIMEWARP = 4
    MAX_STAR_TRAILS = 5
    MAX_LIGHT_PAINTING = 6
    MAX_VEHICLE_LIGHTS = 7


class PhotoMode(GoProEnum):
    SUPER = 0
    NIGHT = 1


class Framing(GoProEnum):
    WIDESCREEN = 0
    VERTICAL = 1
    FULL = 2


class MaxLensModType(GoProEnum):
    NONE = 0
    V1 = 1
    V2 = 2


class Hindsight(GoProEnum):
    SEC_15 = 2
    SEC_30 = 3
    OFF = 4


class PhotoInterval(GoProEnum):
    OFF = 0
    SEC_0_5 = 2
    SEC_1 = 3
    SEC_2 = 4
    SEC_5 = 5
    SEC_10 = 6
    SEC_30 = 7
    SEC_60 = 8
    SEC_120 = 9
    SEC_3 = 10


class PhotoDuration(GoProEnum):
    OFF = 0
    SEC_15 = 1
    SEC_30 = 2
    MIN_1 = 3
    MIN_5 = 4
    MIN_15 = 5
    MIN_30 = 6
    HOUR_1 = 7
    HOUR_2 = 8
    HOUR_3 = 9
