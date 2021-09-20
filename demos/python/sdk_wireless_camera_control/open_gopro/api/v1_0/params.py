# params.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=missing-class-docstring

"""Parameter definitions for GoPro BLE and WiFi commands for Open GoPro version 1.0

Note these have to be IntEnum's in order to be correctly built when sending commands
"""

from open_gopro.constants import GoProEnum

# from open_gopro.proto.request_get_preset_status_pb import EnumRegisterPresetStatus


class ParamsV1_0:
    class Shutter(GoProEnum):
        ON = 1
        OFF = 0

    class Preset(GoProEnum):
        ACTIVITY = 1
        BURST_PHOTO = 65538
        CINEMATIC = 2
        LIVE_BURST = 65537
        NIGHT_PHOTO = 65539
        NIGHT_LAPSE = 131074
        PHOTO = 65536
        STANDARD = 0
        TIME_LAPSE = 131073
        TIME_WARP = 131072
        MAX_PHOTO = 262144
        MAX_TIMEWARP = 327680
        MAX_VIDEO = 196608

    class PresetGroup(GoProEnum):
        VIDE0 = 1000
        PHOTO = 1001
        TIMELAPSE = 1002

    class Resolution(GoProEnum):
        NOT_APPLICABLE = 0
        RES_4K = 1
        RES_2_7K = 4
        RES_2_7K_4_3 = 6
        RES_1440 = 7
        RES_1080 = 9
        RES_4K_4_3 = 18
        RES_5_K = 24

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
        MIN_5 = 4
        MIN_15 = 6
        MIN_30 = 7

    class LensMode(GoProEnum):
        SINGLE = 0
        DUAL = 5

    class VideoFOV(GoProEnum):
        WIDE = 0
        NARROW = 6
        SUPERVIEW = 3
        LINEAR = 4
        MAX_SUPERVIEW = 7
        LINEAR_HORIZON = 8

    class PhotoFOV(GoProEnum):
        NOT_APPLICABLE = 0
        WIDE = 22
        LINEAR = 23
        NARROW = 24
        MAX_SUPERVIEW = 25

    class MultishotFOV(GoProEnum):
        NOT_APPLICABLE = 0
        WIDE = 22
        LINEAR = 23
        NARROW = 24

    class LED(GoProEnum):
        ALL_OFF = 0
        FRONT_OFF = 1
        ALL_ON = 2
        BLE_KEEP_ALIVE = 66

    class PairState(GoProEnum):
        SUCCESS = 0
        IN_PROGRESS = 1
        FAILED = 2
        STOPPED = 3

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
        VIDEO = 12
        LOOPING = 15
        SINGLE_PHOTO = 16
        NIGHT_PHOTO = 18
        BURST_PHOTO = 19
        TIME_LAPSE_VIDEO = 13
        TIME_LAPSE_PHOTO = 20
        NIGHT_LAPSE_PHOTO = 21
        TIME_WARP_VIDEO = 24
        LIVE_BURST = 25
        NIGHT_LAPSE_VIDEO = 26
        SLO_MO = 27

    class Toggle(GoProEnum):
        ENABLE = 1
        DISABLE = 0
