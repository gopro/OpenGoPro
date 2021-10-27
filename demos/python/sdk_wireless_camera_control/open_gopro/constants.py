# constants.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Constant numbers shared across the GoPro module. These do not change across Open GoPro Versions"""

from enum import Enum, EnumMeta
from typing import Union, Tuple, Iterator, Type, TypeVar

import construct

from open_gopro.ble import UUID

T = TypeVar("T")

GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"


class GoProEnumMeta(EnumMeta):
    """Modify enum metaclass to build GoPro specific enums"""

    ITER_SKIP_NAMES = ["NOT_APPLICABLE"]

    def __iter__(cls: Type[T]) -> Iterator[T]:
        """Do not return enum values whose name is in the ITER_SKIP_NAMES list

        Returns:
            Iterator[T]: enum iterator
        """
        return iter([x[1] for x in cls._member_map_.items() if x[0] not in GoProEnumMeta.ITER_SKIP_NAMES])  # type: ignore


class GoProEnum(Enum, metaclass=GoProEnumMeta):
    """GoPro specific enum to be used for all settings, statuses, and parameters

    The name NOT_APPLICABLE is special as it will not be returned as part of the enum iterator
    """


class ErrorCode(GoProEnum):
    """Status Codes."""

    SUCCESS = 0
    ERROR = 1
    INVALID_PARAM = 2


class CmdId(GoProEnum):
    """Command ID's that are written to UUID.CQ_COMMAND."""

    SET_SHUTTER = 0x01
    POWER_DOWN = 0x04
    SLEEP = 0x05
    SET_PAIRING_COMPLETE = 0x03
    GET_CAMERA_SETTINGS = 0x12
    GET_CAMERA_STATUSES = 0x13
    SET_WIFI = 0x17
    GET_SETTINGS_JSON = 0x3B
    GET_HW_INFO = 0x3C
    LOAD_PRESET_GROUP = 0x3E
    LOAD_PRESET = 0x40
    SET_THIRD_PARTY_CLIENT_INFO = 0x50
    GET_THIRD_PARTY_API_VERSION = 0x51
    SET_TURBO_MODE = 0xF1
    GET_PRESET_STATUS = 0xF5


class ActionId(GoProEnum):
    """Action ID's that identify a protobuf command."""

    SET_TURBO_MODE = 0x6B
    GET_PRESET_STATUS = 0x02


class SettingId(GoProEnum):
    """Setting ID's that identify settings and are written to UUID.CQ_SETTINGS."""

    RESOLUTION = 2
    FPS = 3
    INTERNAL_5 = 5
    INTERNAL_6 = 6
    INTERNAL_13 = 13
    INTERNAL_19 = 19
    INTERNAL_24 = 24
    INTERNAL_30 = 30
    INTERNAL_31 = 31
    INTERNAL_32 = 32
    INTERNAL_37 = 37
    INTERNAL_41 = 41
    INTERNAL_42 = 42
    INTERNAL_43 = 43
    INTERNAL_44 = 44
    INTERNAL_45 = 45
    INTERNAL_47 = 47
    INTERNAL_48 = 48
    INTERNAL_54 = 54
    AUTO_OFF = 59
    INTERNAL_60 = 60
    INTERNAL_61 = 61
    INTERNAL_62 = 62
    INTERNAL_64 = 64
    INTERNAL_65 = 65
    INTERNAL_66 = 66
    INTERNAL_67 = 67
    INTERNAL_68 = 68
    INTERNAL_69 = 69
    INTERNAL_75 = 75
    INTERNAL_76 = 76
    INTERNAL_79 = 79
    INTERNAL_83 = 83
    INTERNAL_84 = 84
    INTERNAL_85 = 85
    INTERNAL_86 = 86
    INTERNAL_87 = 87
    INTERNAL_88 = 88
    LED = 91
    INTERNAL_96 = 96
    INTERNAL_102 = 102
    INTERNAL_103 = 103
    INTERNAL_104 = 104
    INTERNAL_105 = 105
    INTERNAL_106 = 106
    INTERNAL_111 = 111
    INTERNAL_112 = 112
    INTERNAL_114 = 114
    INTERNAL_115 = 115
    INTERNAL_116 = 116
    INTERNAL_117 = 117
    INTERNAL_118 = 118
    VIDEO_FOV = 121
    PHOTO_FOV = 122
    MULTI_SHOT_FOV = 123
    INTERNAL_124 = 124
    INTERNAL_125 = 125
    INTERNAL_126 = 126
    INTERNAL_128 = 128
    SHORTCUT_LOWER_LEFT = 129
    SHORTCUT_LOWER_RIGHT = 130
    SHORTCUT_UPPER_LEFT = 131
    SHORTCUT_UPPER_RIGHT = 132
    INTERNAL_133 = 133
    INTERNAL_134 = 134
    INTERNAL_135 = 135
    INTERNAL_139 = 139
    INTERNAL_144 = 144
    INTERNAL_145 = 145
    INTERNAL_146 = 146
    INTERNAL_147 = 147
    INTERNAL_148 = 148
    INTERNAL_149 = 149
    INTERNAL_153 = 153
    INTERNAL_154 = 154
    INTERNAL_155 = 155
    INTERNAL_156 = 156
    INTERNAL_157 = 157
    INTERNAL_158 = 158
    INTERNAL_159 = 159
    INTERNAL_160 = 160
    INTERNAL_161 = 161
    MAX_LENS_MOD = 162
    INTERNAL_163 = 163
    INTERNAL_164 = 164
    INTERNAL_165 = 165
    INTERNAL_166 = 166
    INTERNAL_167 = 167
    INTERNAL_168 = 168
    INTERNAL_169 = 169
    VIDEO_PERFORMANCE_MODE = 173
    INVALID_FOR_TESTING = 0xFF


class QueryCmdId(GoProEnum):
    """Command ID that is written to UUID.CQ_QUERY."""

    GET_SETTING_VAL = 0x12
    GET_STATUS_VAL = 0x13
    GET_SETTING_NAME = 0x22
    GET_CAPABILITIES_VAL = 0x32
    GET_CAPABILITIES_NAME = 0x42
    REG_SETTING_VAL_UPDATE = 0x52
    REG_STATUS_VAL_UPDATE = 0x53
    REG_CAPABILITIES_UPDATE = 0x62
    UNREG_SETTING_VAL_UPDATE = 0x72
    UNREG_STATUS_VAL_UPDATE = 0x73
    UNREG_CAPABILITIES_UPDATE = 0x82
    SETTING_VAL_PUSH = 0x92
    STATUS_VAL_PUSH = 0x93
    SETTING_CAPABILITY_PUSH = 0xA2
    INVALID_FOR_TESTING = 0xFF


class StatusId(GoProEnum):
    """Status ID to identify statuses sent to UUID.CQ_QUERY or received from UUID.CQ_QUERY_RESP."""

    BATT_PRESENT = 1
    BATT_LEVEL = 2
    EXT_BATT_PRESENT = 3
    EXT_BATT_LEVEL = 4
    SYSTEM_HOT = 6
    SYSTEM_BUSY = 8
    QUICK_CAPTURE = 9
    ENCODING = 10
    LCD_LOCK_ACTIVE = 11
    VIDEO_PROGRESS = 13
    INTERNAL_14 = 14
    WIRELESS_ENABLED = 17
    PAIR_STATE = 19
    PAIR_TYPE = 20
    PAIR_TIME = 21
    WAP_SCAN_STATE = 22
    WAP_SCAN_TIME = 23
    WAP_PROV_STAT = 24
    REMOTE_CTRL_VER = 26
    REMOTE_CTRL_CONN = 27
    PAIR_STATE2 = 28
    WLAN_SSID = 29
    AP_SSID = 30
    APP_COUNT = 31
    PREVIEW_ENABLED = 32
    SD_STATUS = 33
    PHOTOS_REM = 34
    VIDEO_REM = 35
    NUM_GROUP_PHOTO = 36
    NUM_GROUP_VIDEO = 37
    NUM_TOTAL_PHOTO = 38
    NUM_TOTAL_VIDEO = 39
    DATE_TIME = 40
    OTA_STAT = 41
    DOWNLAD_CANCEL_PEND = 42
    MODE_GROUP = 43
    LOCATE_ACTIVE = 45
    INTERNAL_46 = 46
    INTERNAL_47 = 47
    INTERNAL_48 = 48
    MULTI_COUNT_DOWN = 49
    SPACE_REM = 54
    STREAMING_SUPP = 55
    WIFI_BARS = 56
    CURRENT_TIME_MS = 57
    NUM_HILIGHTS = 58
    LAST_HILIGHT = 59
    NEXT_POLL = 60
    ANALYTICS_RDY = 61
    ANALYTICS_SIZE = 62
    IN_CONTEXT_MENU = 63
    TIMELAPSE_REM = 64
    EXPOSURE_TYPE = 65
    EXPOSURE_X = 66
    EXPOSURE_Y = 67
    GPS_STAT = 68
    AP_STATE = 69
    INT_BATT_PER = 70
    ACC_MIC_STAT = 74
    DIGITAL_ZOOM = 75
    WIRELESS_BAND = 76
    DIG_ZOOM_ACTIVE = 77
    MOBILE_VIDEO = 78
    FIRST_TIME = 79
    SEC_SD_STAT = 80
    BAND_5GHZ_AVAIL = 81
    SYSTEM_READY = 82
    BATT_OK_OTA = 83
    CAPTURE_DELAY = 84
    VIDEO_LOW_TEMP = 85
    ORIENTATION = 86
    THERMAL_MIT_MODE = 87
    ZOOM_ENCODING = 88
    FLATMODE_ID = 89
    INTERNAL_90 = 90
    LOGS_READY = 91
    TIMEWARP_1X_ACTIVE = 92
    VIDEO_PRESETS = 93
    PHOTO_PRESETS = 94
    TIMELAPSE_PRESETS = 95
    PRESETS_GROUP = 96
    ACTIVE_PRESET = 97
    PRESET_MODIFIED = 98
    LIVE_BURST_REM = 99
    LIVE_BURST_TOTAL = 100
    CAPT_DELAY_ACTIVE = 101
    MEDIA_MOD_MIC_STAT = 102
    TIMEWARP_SPEED_RAMP = 103
    LINUX_CORE_ACTIVE = 104
    CAMERA_LENS_TYPE = 105
    VIDEO_HINDSIGHT = 106
    SCHEDULED_PRESET = 107
    SCHEDULED_CAPTURE = 108
    CREATING_PRESET = 109
    MEDIA_MOD_STAT = 110
    SD_RATING_CHECK_ERROR = 111
    SD_WRITE_SPEED_ERROR = 112
    TURBO_MODE = 113
    CAMERA_CONTROL = 114
    USB_CONNECTED = 115


ProducerType = Tuple[QueryCmdId, Union[SettingId, StatusId]]
"""Types that can be registered for."""

CmdType = Union[CmdId, QueryCmdId, ActionId]
"""Types that identify a command."""

ResponseType = Union[CmdType, StatusId, SettingId, UUID, str, construct.Enum]
"""Types that are used to identify a response."""
