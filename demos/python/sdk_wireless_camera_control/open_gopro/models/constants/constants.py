# constants.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Constant numbers shared across the GoPro module. These do not change across Open GoPro Versions"""

# pylint: disable=missing-class-docstring, no-member

from __future__ import annotations

from open_gopro.domain.enum import GoProIntEnum


class ErrorCode(GoProIntEnum):
    """Status Codes."""

    SUCCESS = 0
    ERROR = 1
    INVALID_PARAM = 2
    UNKNOWN = -1


class CmdId(GoProIntEnum):
    """Command ID's that are written to GoProUUID.CQ_COMMAND."""

    SET_SHUTTER = 0x01
    POWER_DOWN = 0x04
    SLEEP = 0x05
    SET_PAIRING_COMPLETE = 0x03
    SET_DATE_TIME = 0x0D
    GET_DATE_TIME = 0x0E
    SET_DATE_TIME_DST = 0x0F
    GET_DATE_TIME_DST = 0x10
    REBOOT = 0x11
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


class ActionId(GoProIntEnum):
    """Action ID's that identify a protobuf command."""

    SET_PAIRING_STATE = 0x01
    SCAN_WIFI_NETWORKS = 0x02
    GET_AP_ENTRIES = 0x03
    REQUEST_WIFI_CONNECT = 0x04
    REQUEST_WIFI_CONNECT_NEW = 0x05
    NOTIF_START_SCAN = 0x0B
    NOTIF_PROVIS_STATE = 0x0C
    REQUEST_PRESET_UPDATE_CUSTOM = 0x64
    SET_CAMERA_CONTROL = 0x69
    SET_TURBO_MODE = 0x6B
    GET_PRESET_STATUS = 0x72
    GET_LIVESTREAM_STATUS = 0x74
    RELEASE_NETWORK = 0x78
    SET_LIVESTREAM_MODE = 0x79
    SET_PAIRING_STATE_RSP = 0x81
    SCAN_WIFI_NETWORKS_RSP = 0x82
    GET_AP_ENTRIES_RSP = 0x83
    REQUEST_WIFI_CONNECT_RSP = 0x84
    REQUEST_WIFI_CONNECT_NEW_RSP = 0x85
    REQUEST_COHN_SETTING = 0x65
    REQUEST_CLEAR_COHN_CERT = 0x66
    REQUEST_CREATE_COHN_CERT = 0x67
    REQUEST_GET_LAST_MEDIA = 0x6D
    REQUEST_GET_COHN_CERT = 0x6E
    REQUEST_GET_COHN_STATUS = 0x6F
    RESPONSE_PRESET_UPDATE_CUSTOM = 0xE4
    RESPONSE_COHN_SETTING = 0xE5
    RESPONSE_CLEAR_COHN_CERT = 0xE6
    RESPONSE_CREATE_COHN_CERT = 0xE7
    SET_CAMERA_CONTROL_RSP = 0xE9
    SET_TURBO_MODE_RSP = 0xEB
    RESPONSE_GET_LAST_MEDIA = 0xED
    RESPONSE_GET_COHN_CERT = 0xEE
    RESPONSE_GET_COHN_STATUS = 0xEF
    GET_PRESET_STATUS_RSP = 0xF2
    PRESET_MODIFIED_NOTIFICATION = 0xF3
    LIVESTREAM_STATUS_RSP = 0xF4
    LIVESTREAM_STATUS_NOTIF = 0xF5
    RELEASE_NETWORK_RSP = 0xF8
    SET_LIVESTREAM_MODE_RSP = 0xF9
    INTERNAL_FF = 0xFF


class FeatureId(GoProIntEnum):
    """ID's that group protobuf commands"""

    NETWORK_MANAGEMENT = 0x02
    WIRELESS_MANAGEMENT = 0x03
    COMMAND = 0xF1
    SETTING = 0xF3
    QUERY = 0xF5


class QueryCmdId(GoProIntEnum):
    """Command ID that is written to GoProUUID.CQ_QUERY."""

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


class Toggle(GoProIntEnum):
    """A booleanesque enum"""

    ENABLE = 1
    DISABLE = 0


class LED_SPECIAL(GoProIntEnum):
    """Special (not functional) LED value used for keep alive signal"""

    BLE_KEEP_ALIVE = 66


class CameraControl(GoProIntEnum):
    """Camera Control Request Values"""

    IDLE = 0
    CAMERA = 1
    EXTERNAL = 2
