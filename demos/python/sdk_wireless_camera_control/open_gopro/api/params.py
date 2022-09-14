# params.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=missing-class-docstring, no-member

"""Parameter definitions for GoPro BLE and WiFi commands for Open GoPro version 2.0"""

from __future__ import annotations

from open_gopro.constants import GoProEnum

# Import required parameters from protobuf
import open_gopro.proto.live_streaming_pb2
import open_gopro.proto.network_management_pb2
import open_gopro.proto.request_get_preset_status_pb2
import open_gopro.proto.set_camera_control_status_pb2


class LiveStreamStatus(GoProEnum):
    IDLE = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_IDLE
    CONFIG = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_CONFIG
    READY = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_READY
    STREAMING = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_STREAMING
    STAY_ON_COMPLETE = (
        open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_COMPLETE_STAY_ON
    )
    STAY_ON_FAILED = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_FAILED_STAY_ON
    RECONNECTING = open_gopro.proto.live_streaming_pb2.EnumLiveStreamStatus.LIVE_STREAM_STATE_RECONNECTING


class LensType(GoProEnum):
    WIDE = open_gopro.proto.live_streaming_pb2.EnumLens.LENS_WIDE
    LINEAR = open_gopro.proto.live_streaming_pb2.EnumLens.LENS_LINEAR
    SUPERVIEW = open_gopro.proto.live_streaming_pb2.EnumLens.LENS_SUPERVIEW


class WindowSize(GoProEnum):
    SIZE_480 = open_gopro.proto.live_streaming_pb2.EnumWindowSize.WINDOW_SIZE_480
    SIZE_720 = open_gopro.proto.live_streaming_pb2.EnumWindowSize.WINDOW_SIZE_720
    SIZE_1080 = open_gopro.proto.live_streaming_pb2.EnumWindowSize.WINDOW_SIZE_1080


class ProvisioningState(GoProEnum):
    UNKNOWN = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_UNKNOWN
    NEVER_STARTED = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_NEVER_STARTED
    STARTED = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_STARTED
    ABORTED_BY_SYSTEM = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ABORTED_BY_SYSTEM
    CANCELLED_BY_USER = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_CANCELLED_BY_USER
    SUCCESS_NEW_AP = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
    SUCCESS_OLD_AP = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_SUCCESS_OLD_AP
    ERROR_FAILED_TO_ASSOCIATE = (
        open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ERROR_FAILED_TO_ASSOCIATE
    )
    ERROR_PASSWORD_AUTH = (
        open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ERROR_PASSWORD_AUTH
    )
    ERROR_EULA_BLOCKING = (
        open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ERROR_EULA_BLOCKING
    )
    ERROR_NO_INTERNET = open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ERROR_NO_INTERNET
    ERROR_UNSUPPORTED_TYPE = (
        open_gopro.proto.network_management_pb2.EnumProvisioning.PROVISIONING_ERROR_UNSUPPORTED_TYPE
    )


class RegisterPreset(GoProEnum):
    PRESET = (
        open_gopro.proto.request_get_preset_status_pb2.EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET
    )
    PRESET_GROUP_ARRAY = (
        open_gopro.proto.request_get_preset_status_pb2.EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY
    )


class RegisterLiveStream(GoProEnum):
    MODE = open_gopro.proto.live_streaming_pb2.EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_MODE
    ERROR = open_gopro.proto.live_streaming_pb2.EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_ERROR
    STATUS = (
        open_gopro.proto.live_streaming_pb2.EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS
    )


class CameraControlStatus(GoProEnum):
    IDLE = open_gopro.proto.set_camera_control_status_pb2.EnumCameraControlStatus.CAMERA_IDLE
    CONTROL = open_gopro.proto.set_camera_control_status_pb2.EnumCameraControlStatus.CAMERA_CONTROL
    EXTERNAL_CONTROL = (
        open_gopro.proto.set_camera_control_status_pb2.EnumCameraControlStatus.CAMERA_EXTERNAL_CONTROL
    )


class PresetGroup(GoProEnum):
    VIDEO = 1000
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
    RES_5K = 24
    RES_5_K_4_3 = 25
    RES_5_3_K_8_7 = 26
    RES_5_3_K_4_3 = 27
    RES_4_K_8_7 = 28
    RES_5_3_K = 100


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
    NARROW = 2
    SUPERVIEW = 3
    LINEAR = 4
    MAX_SUPERVIEW = 7
    LINEAR_HORIZON_LEVELING = 8
    HYPERVIEW = 9
    LINEAR_HORIZON_LOCK = 10


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


class HypersmoothMode(GoProEnum):
    OFF = 0
    UNKNOWN = 1
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
