# constants.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Constant numbers shared across the GoPro module. These do not change across Open GoPro Versions"""

from __future__ import annotations
from enum import IntEnum, Enum, IntFlag, EnumMeta
from dataclasses import dataclass
from typing import Protocol, Union, Iterator, TypeVar, Any, no_type_check, Final

import construct

from open_gopro.ble import BleUUID, UUIDs

T = TypeVar("T")


##############################################################################################################
#####################   Custom Enum for this Project  ########################################################
##############################################################################################################


class ProtobufDescriptor(Protocol):
    """Protocol definition for Protobuf enum descriptor used to generate GoPro enums from protobufs"""

    @property
    def name(self) -> str:
        """Human readable name of protobuf enum

        # noqa: DAR202

        Returns:
            str: enum name
        """

    @property
    def values_by_name(self) -> dict:
        """Get the enum values by name

        # noqa: DAR202

        Returns:
            dict: Dict of enum values mapped by name
        """

    @property
    def values_by_number(self) -> dict:
        """Get the enum values by number

        # noqa: DAR202

        Returns:
            dict: dict of enum numbers mapped by numberf
        """


class GoProEnumMeta(EnumMeta):
    """Modify enum metaclass to build GoPro specific enums"""

    _is_proto = False
    _iter_skip_names = ("NOT_APPLICABLE", "DESCRIPTOR")

    @no_type_check
    def __new__(cls, name, bases, classdict, **kwargs) -> GoProEnumMeta:  # noqa
        is_proto = "__is_proto__" in classdict
        classdict["_ignore_"] = "__is_proto__"
        classdict["__doc__"] = ""  # Don't use useless "An enumeration" docstring
        e = super().__new__(cls, name, bases, classdict, **kwargs)
        setattr(e, "_is_proto", is_proto)
        return e

    @no_type_check
    def __contains__(cls: type[Any], obj: object) -> bool:
        if isinstance(obj, Enum):
            return super().__contains__(obj)
        if isinstance(obj, int):
            return obj in [x.value for x in cls._member_map_.values()]
        if isinstance(obj, str):
            return obj.lower() in [x.name.lower() for x in cls._member_map_.values()]
        raise TypeError(
            f"unsupported operand type(s) for 'in': {type(obj).__qualname__} and {cls.__class__.__qualname__}"
        )

    def __iter__(cls: type[T]) -> Iterator[T]:
        """Do not return enum values whose name is in the _iter_skip_names list

        Returns:
            Iterator[T]: enum iterator
        """
        return iter([x[1] for x in cls._member_map_.items() if x[0] not in GoProEnumMeta._iter_skip_names])  # type: ignore


class GoProFlagEnum(IntFlag, metaclass=GoProEnumMeta):
    """GoPro specific enum to be used for all settings, statuses, and parameters

    The names NOT_APPLICABLE and DESCRIPTOR are special as they will not be returned as part of the enum iterator
    """

    def __eq__(self, other: object) -> bool:
        if type(self)._is_proto:
            if isinstance(other, int):
                return self.value == other
            if isinstance(other, str):
                return self.name == other
            if isinstance(other, Enum):
                return self.value == other.value
            raise TypeError(f"Unexpected case: proto enum can only be str or int, not {type(other)}")
        return super().__eq__(other)

    def __hash__(self) -> Any:
        return hash(self.name or "" + str(self.value))


class GoProEnum(IntEnum, metaclass=GoProEnumMeta):
    """GoPro specific enum to be used for all settings, statuses, and parameters

    The names NOT_APPLICABLE and DESCRIPTOR are special as they will not be returned as part of the enum iterator
    """

    def __eq__(self, other: object) -> bool:
        if type(self)._is_proto:
            if isinstance(other, int):
                return self.value == other
            if isinstance(other, str):
                return self.name == other
            if isinstance(other, Enum):
                return self.value == other.value
            raise TypeError(f"Unexpected case: proto enum can only be str or int, not {type(other)}")
        return super().__eq__(other)

    def __hash__(self) -> Any:
        return hash(self.name + str(self.value))


def enum_factory(proto_enum: ProtobufDescriptor) -> type[GoProEnum]:
    """Dynamically build a GoProEnum from a protobuf enum

    Args:
        proto_enum (ProtobufDescriptor): input protobuf enum descriptor

    Returns:
        GoProEnum: generated GoProEnum
    """
    return GoProEnum(  # type: ignore # pylint: disable=too-many-function-args
        proto_enum.name,  # type: ignore
        {
            **dict(
                zip(
                    proto_enum.values_by_name.keys(),
                    proto_enum.values_by_number.keys(),
                )
            ),
            "__is_proto__": True,
        },
    )


##############################################################################################################
#####################  End Enum Definition ###################################################################
##############################################################################################################

GOPRO_BASE_UUID: Final = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"


@dataclass(frozen=True)
class GoProUUIDs(UUIDs):
    """GoPro Proprietary BleUUID's."""

    # GoPro Wifi Access Point Service
    S_WIFI_ACCESS_POINT = BleUUID("Wifi Access Point Service", hex=GOPRO_BASE_UUID.format("0001"))
    WAP_SSID = BleUUID("Wifi AP SSID", hex=GOPRO_BASE_UUID.format("0002"))
    WAP_PASSWORD = BleUUID("Wifi AP Password", hex=GOPRO_BASE_UUID.format("0003"))
    WAP_POWER = BleUUID("Wifi Power", hex=GOPRO_BASE_UUID.format("0004"))
    WAP_STATE = BleUUID("Wifi State", hex=GOPRO_BASE_UUID.format("0005"))
    WAP_CSI_PASSWORD = BleUUID("CSI Password", hex=GOPRO_BASE_UUID.format("0006"))

    # GoPro Control & Query Service
    S_CONTROL_QUERY = BleUUID("Control and Query Service", hex="0000fea6-0000-1000-8000-00805f9b34fb")
    CQ_COMMAND = BleUUID("Command", hex=GOPRO_BASE_UUID.format("0072"))
    CQ_COMMAND_RESP = BleUUID("Command Response", hex=GOPRO_BASE_UUID.format("0073"))
    CQ_SETTINGS = BleUUID("Settings", hex=GOPRO_BASE_UUID.format("0074"))
    CQ_SETTINGS_RESP = BleUUID("Settings Response", hex=GOPRO_BASE_UUID.format("0075"))
    CQ_QUERY = BleUUID("Query", hex=GOPRO_BASE_UUID.format("0076"))
    CQ_QUERY_RESP = BleUUID("Query Response", hex=GOPRO_BASE_UUID.format("0077"))
    CQ_SENSOR = BleUUID("Sensor", hex=GOPRO_BASE_UUID.format("0078"))
    CQ_SENSOR_RESP = BleUUID("Sensor Response", hex=GOPRO_BASE_UUID.format("0079"))

    # GoPro Camera Management Service
    S_CAMERA_MANAGEMENT = BleUUID("Camera Management Service", hex=GOPRO_BASE_UUID.format("0090"))
    CM_NET_MGMT_COMM = BleUUID("Camera Management", hex=GOPRO_BASE_UUID.format("0091"))
    CN_NET_MGMT_RESP = BleUUID("Camera Management Response", hex=GOPRO_BASE_UUID.format("0092"))

    # Unknown
    S_INTERNAL = BleUUID("Unknown Service", hex=GOPRO_BASE_UUID.format("0080"))
    INTERNAL_81 = BleUUID("Internal 81", hex=GOPRO_BASE_UUID.format("0081"))
    INTERNAL_82 = BleUUID("Internal 82", hex=GOPRO_BASE_UUID.format("0082"))
    INTERNAL_83 = BleUUID("Internal 83", hex=GOPRO_BASE_UUID.format("0083"))
    INTERNAL_84 = BleUUID("Internal 84", hex=GOPRO_BASE_UUID.format("0084"))


class ErrorCode(GoProEnum):
    """Status Codes."""

    SUCCESS = 0
    ERROR = 1
    INVALID_PARAM = 2
    UNKNOWN = -1


class CmdId(GoProEnum):
    """Command ID's that are written to GoProUUIDs.CQ_COMMAND."""

    SET_SHUTTER = 0x01
    POWER_DOWN = 0x04
    SLEEP = 0x05
    SET_PAIRING_COMPLETE = 0x03
    SET_DATE_TIME = 0x0D
    GET_DATE_TIME = 0x0E
    SET_DATE_TIME_DST = 0x0F
    GET_DATE_TIME_DST = 0x10
    GET_CAMERA_SETTINGS = 0x12
    GET_CAMERA_STATUSES = 0x13
    GET_CAMERA_CAPABILITIES = 0x32
    SET_WIFI = 0x17
    TAG_HILIGHT = 0x18
    GET_SETTINGS_JSON = 0x3B
    GET_HW_INFO = 0x3C
    LOAD_PRESET_GROUP = 0x3E
    LOAD_PRESET = 0x40
    SET_THIRD_PARTY_CLIENT_INFO = 0x50
    GET_THIRD_PARTY_API_VERSION = 0x51
    REGISTER_ALL_SETTINGS = 0x52
    REGISTER_ALL_STATUSES = 0x53
    UNREGISTER_ALL_SETTINGS = 0x72
    UNREGISTER_ALL_STATUSES = 0x73
    REGISTER_ALL_CAPABILITIES = 0x62
    UNREGISTER_ALL_CAPABILITIES = 0x82


class ActionId(GoProEnum):
    """Action ID's that identify a protobuf command."""

    SCAN_WIFI_NETWORKS = 0x02
    GET_AP_ENTRIES = 0x03
    REQUEST_WIFI_CONNECT = 0x05
    NOTIF_START_SCAN = 0x0B
    NOTIF_PROVIS_STATE = 0x0C
    SET_CAMERA_CONTROL = 0x69
    SET_TURBO_MODE = 0x6B
    GET_PRESET_STATUS = 0x72
    GET_LIVESTREAM_STATUS = 0x74
    RELEASE_NETWORK = 0x78
    SET_LIVESTREAM_MODE = 0x79
    SCAN_WIFI_NETWORKS_RSP = 0x82
    GET_AP_ENTRIES_RSP = 0x83
    REQUEST_WIFI_CONNECT_RSP = 0x85
    SET_CAMERA_CONTROL_RSP = 0xE9
    SET_TURBO_MODE_RSP = 0xEB
    GET_PRESET_STATUS_RSP = 0xF2
    PRESET_MODIFIED_NOTIFICATION = 0xF3
    LIVESTREAM_STATUS_RSP = 0xF4
    LIVESTREAM_STATUS_NOTIF = 0xF5
    RELEASE_NETWORK_RSP = 0xF8
    SET_LIVESTREAM_MODE_RSP = 0xF9
    INTERNAL_FF = 0xFF


class FeatureId(GoProEnum):
    """ID's that group protobuf commands"""

    NETWORK_MANAGEMENT = 0x02
    COMMAND = 0xF1
    SETTING = 0xF3
    QUERY = 0xF5


class SettingId(GoProEnum):
    """Setting ID's that identify settings and are written to GoProUUIDs.CQ_SETTINGS."""

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
    MEDIA_FORMAT = 128
    INTERNAL_129 = 129
    INTERNAL_130 = 130
    INTERNAL_131 = 131
    INTERNAL_132 = 132
    INTERNAL_133 = 133
    ANTI_FLICKER = 134
    HYPERSMOOTH = 135
    INTERNAL_139 = 139
    INTERNAL_142 = 142
    INTERNAL_144 = 144
    INTERNAL_145 = 145
    INTERNAL_146 = 146
    INTERNAL_147 = 147
    INTERNAL_148 = 148
    INTERNAL_149 = 149
    VIDEO_HORIZON_LEVELING = 150
    PHOTO_HORIZON_LEVELING = 151
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
    INTERNAL_174 = 174
    CAMERA_UX_MODE = 175
    VIDEO_EASY_MODE = 176
    PHOTO_EASY_MODE = 177
    WIFI_BAND = 178
    STAR_TRAIL_LENGTH = 179
    SYSTEM_VIDEO_MODE = 180
    INTERNAL_181 = 181
    PROTOBUF_SETTING = 0xF3
    INVALID_FOR_TESTING = 0xFF


class QueryCmdId(GoProEnum):
    """Command ID that is written to GoProUUIDs.CQ_QUERY."""

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
    PROTOBUF_QUERY = 0xF5
    INVALID_FOR_TESTING = 0xFF


class StatusId(GoProEnum):
    """Status ID to identify statuses sent to GoProUUIDs.CQ_QUERY or received from GoProUUIDs.CQ_QUERY_RESP."""

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
    DEPRECATED_40 = 40
    OTA_STAT = 41
    DOWNLOAD_CANCEL_PEND = 42
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
    DEPRECATED_87 = 87
    ZOOM_ENCODING = 88
    FLATMODE_ID = 89
    INTERNAL_90 = 90
    LOGS_READY = 91
    DEPRECATED_92 = 92
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
    CONTROL_OVER_USB = 116
    TOTAL_SD_SPACE_KB = 117


ProducerType = tuple[QueryCmdId, Union[SettingId, StatusId]]
"""Types that can be registered for."""

CmdType = Union[CmdId, QueryCmdId, ActionId]
"""Types that identify a command."""

ResponseType = Union[CmdType, StatusId, SettingId, BleUUID, str, construct.Enum]
"""Types that are used to identify a response."""
