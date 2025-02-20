"""Status-related constants"""

########################################################################################################################
#
# Warning!! This file is auto-generated. Do not modify it manually.
#
########################################################################################################################

from open_gopro.enum import GoProIntEnum


class StatusId(GoProIntEnum):
    """Status ID to identify statuses sent to GoProUUID.CQ_QUERY or received from GoProUUID.CQ_QUERY_RESP."""

    BATTERY_PRESENT = 1
    INTERNAL_BATTERY_BARS = 2
    EXTERNAL_BATTERY = 3
    EXTERNAL_BATTERY_PERCENTAGE = 4
    OVERHEATING = 6
    BUSY = 8
    QUICK_CAPTURE = 9
    ENCODING = 10
    LCD_LOCK = 11
    VIDEO_ENCODING_DURATION = 13
    BROADCAST_DURATION = 14
    WIRELESS_CONNECTIONS_ENABLED = 17
    PAIRING_STATE = 19
    LAST_PAIRING_TYPE = 20
    LAST_PAIRING_SUCCESS = 21
    WIFI_SCAN_STATE = 22
    LAST_WIFI_SCAN_SUCCESS = 23
    WIFI_PROVISIONING_STATE = 24
    REMOTE_VERSION = 26
    REMOTE_CONNECTED = 27
    CONNECTED_WIFI_SSID = 29
    ACCESS_POINT_SSID = 30
    CONNECTED_DEVICES = 31
    PREVIEW_STREAM = 32
    PRIMARY_STORAGE = 33
    REMAINING_PHOTOS = 34
    REMAINING_VIDEO_TIME = 35
    GROUP_PHOTOS = 36
    CHAPTERED_VIDEOS = 37
    PHOTOS = 38
    VIDEOS = 39
    OTA = 41
    PENDING_FW_UPDATE_CANCEL = 42
    LOCATE = 45
    TIMELAPSE_INTERVAL_COUNTDOWN = 49
    SD_CARD_REMAINING = 54
    PREVIEW_STREAM_AVAILABLE = 55
    WIFI_BARS = 56
    ACTIVE_HILIGHTS = 58
    TIME_SINCE_LAST_HILIGHT = 59
    MINIMUM_STATUS_POLL_PERIOD = 60
    ANALYTICS = 61
    ANALYTICS_SIZE = 62
    IN_CONTEXTUAL_MENU = 63
    LIVEVIEW_EXPOSURE_SELECT_MODE = 65
    LIVEVIEW_Y = 66
    LIVEVIEW_X = 67
    GPS_LOCK = 68
    AP_MODE = 69
    INTERNAL_BATTERY_PERCENTAGE = 70
    MICROPHONE_ACCESSORY = 74
    ZOOM_LEVEL = 75
    WIRELESS_BAND = 76
    ZOOM_AVAILABLE = 77
    MOBILE_FRIENDLY = 78
    FTU = 79
    NUM_5GHZ_AVAILABLE = 81
    READY = 82
    OTA_CHARGED = 83
    COLD = 85
    ROTATION = 86
    ZOOM_WHILE_ENCODING = 88
    FLATMODE = 89
    DEFAULT_PROTUNE = 90
    LOGS_READY = 91
    VIDEO_PRESET = 93
    PHOTO_PRESET = 94
    TIMELAPSE_PRESET = 95
    PRESET_GROUP = 96
    PRESET = 97
    PRESET_MODIFIED = 98
    REMAINING_LIVE_BURSTS = 99
    LIVE_BURSTS = 100
    CAPTURE_DELAY_ACTIVE = 101
    MEDIA_MOD_STATE = 102
    TIME_WARP_SPEED = 103
    LINUX_CORE = 104
    LENS_TYPE = 105
    HINDSIGHT = 106
    SCHEDULED_CAPTURE_PRESET_ID = 107
    SCHEDULED_CAPTURE = 108
    CUSTOM_PRESET = 109
    DISPLAY_MOD_STATUS = 110
    SD_CARD_WRITE_SPEED_ERROR = 111
    SD_CARD_ERRORS = 112
    TURBO_TRANSFER = 113
    CAMERA_CONTROL_ID = 114
    USB_CONNECTED = 115
    USB_CONTROLLED = 116
    SD_CARD_CAPACITY = 117
    PHOTO_INTERVAL_CAPTURE_COUNT = 118
    CAMERA_LENS_MOD = 119
    POV_PRESET = 120
    SELFIE_PRESET = 121


class InternalBatteryBars(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-bars-2)"""

    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    CHARGING = 4


class PairingState(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-19)"""

    NEVER_STARTED = 0
    STARTED = 1
    ABORTED = 2
    CANCELLED = 3
    COMPLETED = 4


class LastPairingType(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-type-20)"""

    NOT_PAIRING = 0
    PAIRING_APP = 1
    PAIRING_REMOTE_CONTROL = 2
    PAIRING_BLUETOOTH_DEVICE = 3


class WifiScanState(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-scan-state-22)"""

    NEVER_STARTED = 0
    STARTED = 1
    ABORTED = 2
    CANCELED = 3
    COMPLETED = 4


class WifiProvisioningState(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-provisioning-state-24)"""

    NEVER_STARTED = 0
    STARTED = 1
    ABORTED = 2
    CANCELED = 3
    COMPLETED = 4


class PrimaryStorage(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#primary-storage-33)"""

    UNKNOWN = -1
    OK = 0
    SD_CARD_FULL = 1
    SD_CARD_REMOVED = 2
    SD_CARD_FORMAT_ERROR = 3
    SD_CARD_BUSY = 4
    SD_CARD_SWAPPED = 8


class Ota(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-41)"""

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


class Analytics(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#analytics-61)"""

    NOT_READY = 0
    READY = 1
    ON_CONNECT = 2


class AnalyticsSize(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#analytics-size-62)"""

    VALUE_HARD_CODED_BY_BOSS_IN_LIBGPCTRLD_SRC_CAMERA_STATUS_CPP = 0


class LiveviewExposureSelectMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-exposure-select-mode-65)"""

    DISABLED = 0
    AUTO = 1
    ISO_LOCK = 2
    HEMISPHERE = 3


class MicrophoneAccessory(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#microphone-accessory-74)"""

    ACCESSORY_NOT_CONNECTED = 0
    ACCESSORY_CONNECTED = 1
    ACCESSORY_CONNECTED_AND_A_MICROPHONE_IS_PLUGGED_INTO_THE_ACCESSORY = 2


class WirelessBand(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-band-76)"""

    NUM_2_4_GHZ = 0
    NUM_5_GHZ = 1


class Rotation(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#rotation-86)"""

    NUM_0_DEGREES_UPRIGHT_ = 0
    NUM_180_DEGREES_UPSIDE_DOWN_ = 1
    NUM_90_DEGREES_LAYING_ON_RIGHT_SIDE_ = 2
    NUM_270_DEGREES_LAYING_ON_LEFT_SIDE_ = 3


class MediaModState(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#media-mod-state-102)"""

    MICROPHONE_REMOVED = 0
    MICROPHONE_ONLY = 2
    MICROPHONE_WITH_EXTERNAL_MICROPHONE = 3


class TimeWarpSpeed(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-warp-speed-103)"""

    NUM_15X = 0
    NUM_30X = 1
    NUM_60X = 2
    NUM_150X = 3
    NUM_300X = 4
    NUM_900X = 5
    NUM_1800X = 6
    NUM_2X = 7
    NUM_5X = 8
    NUM_10X = 9
    AUTO = 10
    NUM_1X_REALTIME_ = 11
    NUM_1_2X_SLOW_MOTION_ = 12


class LensType(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lens-type-105)"""

    DEFAULT = 0
    MAX_LENS = 1
    MAX_LENS_2_0 = 2
    MAX_LENS_2_5 = 3
    MACRO_LENS = 4
    ANAMORPHIC_LENS = 5
    NEUTRAL_DENSITY_4 = 6
    NEUTRAL_DENSITY_8 = 7
    NEUTRAL_DENSITY_16 = 8
    NEUTRAL_DENSITY_32 = 9


class DisplayModStatus(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#display-mod-status-110)"""

    NUM_000_DISPLAY_MOD_0_HDMI_0_DISPLAY_MOD_CONNECTED_FALSE = 0
    NUM_001_DISPLAY_MOD_0_HDMI_0_DISPLAY_MOD_CONNECTED_TRUE = 1
    NUM_010_DISPLAY_MOD_0_HDMI_1_DISPLAY_MOD_CONNECTED_FALSE = 2
    NUM_011_DISPLAY_MOD_0_HDMI_1_DISPLAY_MOD_CONNECTED_TRUE = 3
    NUM_100_DISPLAY_MOD_1_HDMI_0_DISPLAY_MOD_CONNECTED_FALSE = 4
    NUM_101_DISPLAY_MOD_1_HDMI_0_DISPLAY_MOD_CONNECTED_TRUE = 5
    NUM_110_DISPLAY_MOD_1_HDMI_1_DISPLAY_MOD_CONNECTED_FALSE = 6
    NUM_111_DISPLAY_MOD_1_HDMI_1_DISPLAY_MOD_CONNECTED_TRUE = 7


class CameraControlId(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-control-id-114)"""

    CAMERA_IDLE_NO_ONE_IS_ATTEMPTING_TO_CHANGE_CAMERA_SETTINGS = 0
    CAMERA_CONTROL_CAMERA_IS_IN_A_MENU_OR_CHANGING_SETTINGS_TO_INTERVENE_APP_MUST_REQUEST_CONTROL = 1
    CAMERA_EXTERNAL_CONTROL_AN_OUTSIDE_ENTITY_APP_HAS_CONTROL_AND_IS_IN_A_MENU_OR_MODIFYING_SETTINGS = 2


class UsbControlled(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-controlled-116)"""

    DISABLED = 0
    ENABLED = 1


class CameraLensMod(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-lens-mod-119)"""

    INVALID = -1
    DEFAULT = 0
    MAX_LENS = 1
    MAX_LENS_2_0 = 2
    MAX_LENS_2_5 = 3
    MACRO_LENS = 4
    ANAMORPHIC_LENS = 5
    NEUTRAL_DENSITY_4 = 6
    NEUTRAL_DENSITY_8 = 7
    NEUTRAL_DENSITY_16 = 8
    NEUTRAL_DENSITY_32 = 9
    CLEAR_GLASS_NONE_ = 10
