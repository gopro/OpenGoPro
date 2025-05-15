# ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""BLE Commands and Asynchronous Responses"""

# mypy: disable-error-code=empty-body

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any, Final

from construct import (
    GreedyBytes,
    GreedyString,
    Hex,
    Int8ub,
    Int16ub,
    Int32ub,
    PaddedString,
    Padding,
    Struct,
    this,
)
from returns.result import ResultE

from open_gopro.api.builders import (
    BleAsyncResponse,
    ble_proto_command,
    ble_read_command,
    ble_register_command,
    ble_write_command,
)
from open_gopro.domain.communicator_interface import (
    BleMessage,
    BleMessages,
    MessageRules,
)
from open_gopro.domain.gopro_observable import GoProObservable
from open_gopro.domain.parser_interface import GlobalParsers, Parser
from open_gopro.models import CameraInfo, GoProResp, TzDstDateTime, constants, proto
from open_gopro.models.constants import (
    ActionId,
    CmdId,
    FeatureId,
    GoProUUID,
    SettingId,
    StatusId,
)
from open_gopro.models.types import CameraState
from open_gopro.parsers.bytes import (
    ConstructByteParserBuilder,
    DateTimeByteParserBuilder,
    ProtobufByteParser,
)
from open_gopro.parsers.json import (
    CameraStateJsonParser,
    LambdaJsonParser,
    PydanticAdapterJsonParser,
)

logger = logging.getLogger(__name__)


class BleCommands(BleMessages[BleMessage]):
    """All of the BLE commands.

    To be used as a delegate for a GoProBle instance to build commands
    """

    ######################################################################################################
    #                          BLE WRITE COMMANDS
    ######################################################################################################

    @ble_write_command(
        uuid=GoProUUID.CQ_COMMAND,
        cmd=CmdId.SET_SHUTTER,
        param_builder=Int8ub,
        rules=MessageRules(
            fastpass_analyzer=lambda **kwargs: kwargs["shutter"] == constants.Toggle.DISABLE,
            wait_for_encoding_analyzer=lambda **kwargs: kwargs["shutter"] == constants.Toggle.ENABLE,
        ),
    )
    async def set_shutter(self, *, shutter: constants.Toggle) -> GoProResp[None]:
        """Set the Shutter to start / stop encoding

        Args:
            shutter (constants.Toggle): on or off

        Returns:
            GoProResp[None]: status of command
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.TAG_HILIGHT)
    async def tag_hilight(self) -> GoProResp[None]:
        """Tag a highlight during encoding

        Returns:
            GoProResp[None]: status of command
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.POWER_DOWN)
    async def power_down(self) -> GoProResp[None]:
        """Power Down the camera

        Returns:
            GoProResp[None]: status of command
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.SLEEP)
    async def sleep(self) -> GoProResp[None]:
        """Put the camera in standby

        Returns:
            GoProResp[None]: status of command
        """

    @ble_write_command(
        uuid=GoProUUID.CQ_COMMAND,
        cmd=CmdId.GET_HW_INFO,
        parser=Parser(
            byte_json_adapter=ConstructByteParserBuilder(
                Struct(
                    Padding(1),
                    "model_number" / Int32ub,
                    "model_name_len" / Int8ub,
                    "model_name" / PaddedString(this.model_name_len, "utf-8"),
                    Padding(1),
                    "board_type" / Hex(Int32ub),
                    "firmware_version_len" / Int8ub,
                    "firmware_version" / PaddedString(this.firmware_version_len, "utf-8"),
                    "serial_number_len" / Int8ub,
                    "serial_number" / PaddedString(this.serial_number_len, "utf-8"),
                    "ap_ssid_len" / Int8ub,
                    "ap_ssid" / PaddedString(this.ap_ssid_len, "utf-8"),
                    "ap_mac_len" / Int8ub,
                    "ap_mac_addr" / PaddedString(this.ap_mac_len, "utf-8"),
                )
            ),
            json_parser=PydanticAdapterJsonParser(CameraInfo),
        ),
    )
    async def get_hardware_info(self) -> GoProResp[CameraInfo]:
        """Get the model number, board, type, firmware version, serial number, and AP info

        Returns:
            GoProResp[CameraInfo]: response as JSON
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.SET_WIFI, Int8ub)
    async def enable_wifi_ap(self, *, enable: bool) -> GoProResp[None]:
        """Enable / disable the Wi-Fi Access Point.

        Args:
            enable (bool): True to enable, False to disable

        Returns:
            GoProResp[None]: response as JSON
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.LOAD_PRESET_GROUP, Int16ub)
    async def load_preset_group(self, *, group: proto.EnumPresetGroup.ValueType) -> GoProResp[None]:
        """Load a Preset Group.

        Once complete, the most recently used preset in this group will be active.

        Args:
            group (proto.EnumPresetGroup.ValueType): preset group to load

        Returns:
            GoProResp[None]: response as JSON
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.LOAD_PRESET, Int32ub)
    async def load_preset(self, *, preset: int) -> GoProResp[None]:
        """Load a Preset

        The integer preset value can be found from the get_preset_status command

        Args:
            preset (int): preset ID to load

        Returns:
            GoProResp[None]: command status
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.SET_THIRD_PARTY_CLIENT_INFO)
    async def set_third_party_client_info(self) -> GoProResp[None]:
        """Flag as third party app

        Returns:
            GoProResp[None]: command status
        """

    @ble_write_command(
        uuid=GoProUUID.CQ_COMMAND,
        cmd=CmdId.GET_THIRD_PARTY_API_VERSION,
        parser=Parser(
            byte_json_adapter=ConstructByteParserBuilder(
                Struct(Padding(1), "major" / Int8ub, Padding(1), "minor" / Int8ub)
            ),
            json_parser=LambdaJsonParser(lambda data: f"{data['major']}.{data['minor']}"),
        ),
    )
    async def get_open_gopro_api_version(self) -> GoProResp[str]:
        """Get Open GoPro API Version

        Returns:
            GoProResp[str]: response as JSON
        """

    @ble_write_command(
        GoProUUID.CQ_QUERY,
        CmdId.GET_CAMERA_STATUSES,
        parser=Parser(json_parser=CameraStateJsonParser()),
    )
    async def get_camera_statuses(self) -> GoProResp[CameraState]:
        """Get all of the camera's statuses

        Returns:
            GoProResp[CameraState]: response as JSON
        """

    @ble_write_command(
        GoProUUID.CQ_QUERY,
        CmdId.GET_CAMERA_SETTINGS,
        parser=Parser(json_parser=CameraStateJsonParser()),
    )
    async def get_camera_settings(self) -> GoProResp[CameraState]:
        """Get all of the camera's settings

        Returns:
            GoProResp[CameraState]: response as JSON
        """

    @ble_write_command(
        GoProUUID.CQ_QUERY,
        CmdId.GET_CAMERA_CAPABILITIES,
        parser=Parser(json_parser=CameraStateJsonParser()),
    )
    async def get_camera_capabilities(self) -> GoProResp[CameraState]:
        """Get the current capabilities of each camera setting

        Returns:
            GoProResp[CameraState]: response as JSON
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.SET_DATE_TIME, param_builder=DateTimeByteParserBuilder())
    async def set_date_time(self, *, date_time: datetime.datetime) -> GoProResp[None]:
        """Set the camera's date and time (non timezone / DST version)

        Args:
            date_time (datetime.datetime): Date and time to set (Timezone will be ignored)

        Returns:
            GoProResp[None]: command status
        """

    @ble_write_command(
        GoProUUID.CQ_COMMAND,
        CmdId.GET_DATE_TIME,
        parser=Parser(
            byte_json_adapter=DateTimeByteParserBuilder(),
            json_parser=LambdaJsonParser(lambda data: data["datetime"]),
        ),
    )
    async def get_date_time(self) -> GoProResp[datetime.datetime]:
        """Get the camera's date and time (non timezone / DST version)

        Returns:
            GoProResp[datetime.datetime]: response as JSON
        """

    @ble_write_command(GoProUUID.CQ_COMMAND, CmdId.SET_DATE_TIME_DST, param_builder=DateTimeByteParserBuilder())
    async def set_date_time_tz_dst(
        self, *, date_time: datetime.datetime, tz_offset: int, is_dst: bool
    ) -> GoProResp[None]:
        """Set the camera's date and time with timezone and DST

        Args:
            date_time (datetime.datetime): date and time
            tz_offset (int): timezone as UTC offset
            is_dst (bool): is daylight savings time?

        Returns:
            GoProResp[None]: command status
        """

    @ble_write_command(
        GoProUUID.CQ_COMMAND,
        CmdId.GET_DATE_TIME_DST,
        parser=Parser(
            byte_json_adapter=DateTimeByteParserBuilder(),
            json_parser=PydanticAdapterJsonParser(TzDstDateTime),
        ),
    )
    async def get_date_time_tz_dst(self) -> GoProResp[TzDstDateTime]:
        """Get the camera's date and time with timezone / DST

        Returns:
            GoProResp[TzDstDateTime]: response as JSON
        """

    @ble_write_command(
        uuid=GoProUUID.CQ_COMMAND,
        cmd=CmdId.REBOOT,
        rules=MessageRules(
            fastpass_analyzer=lambda **_: True,
        ),
    )
    async def reboot(self) -> GoProResp[None]:
        """Reboot the camera (approximating a battery pull)

        Returns:
            GoProResp[None]: Empty response
        """

    ######################################################################################################
    #                          BLE DIRECT CHARACTERISTIC READ COMMANDS
    ######################################################################################################

    @ble_read_command(
        uuid=GoProUUID.WAP_SSID,
        parser=Parser(
            byte_json_adapter=ConstructByteParserBuilder(Struct("ssid" / GreedyString("utf-8"))),
            json_parser=LambdaJsonParser(lambda data: data["ssid"]),
        ),
    )
    async def get_wifi_ssid(self) -> GoProResp[str]:
        """Get the Wifi SSID.

        Returns:
            GoProResp[str]: command status and SSID
        """

    @ble_read_command(
        uuid=GoProUUID.WAP_PASSWORD,
        parser=Parser(
            byte_json_adapter=ConstructByteParserBuilder(Struct("password" / GreedyString("utf-8"))),
            json_parser=LambdaJsonParser(lambda data: data["password"]),
        ),
    )
    async def get_wifi_password(self) -> GoProResp[str]:
        """Get the Wifi password.

        Returns:
            GoProResp[str]: command status and password
        """

    ######################################################################################################
    #                          REGISTER / UNREGISTER ALL COMMANDS
    ######################################################################################################

    @ble_register_command(GoProUUID.CQ_QUERY, CmdId.REGISTER_ALL_STATUSES, update_set=StatusId)
    async def get_observable_for_all_statuses(self) -> ResultE[GoProObservable[dict[StatusId, Any]]]:
        """Register push notifications for all statuses

        Returns:
            ResultE[GoProObservable[dict[StatusId, Any]]]: command status and current value of all statuses
                indexed by StatusId
        """

    @ble_register_command(GoProUUID.CQ_QUERY, CmdId.REGISTER_ALL_SETTINGS, update_set=SettingId)
    async def get_observable_for_all_settings(self) -> ResultE[GoProObservable[dict[SettingId, Any]]]:
        """Register push notifications for all settings

        Returns:
            ResultE[GoProObservable[dict[SettingId, Any]]]: command status and current value of all settings
                indexed by SettingId
        """

    @ble_register_command(GoProUUID.CQ_QUERY, CmdId.REGISTER_ALL_CAPABILITIES, update_set=SettingId)
    async def get_observable_for_all_capabilities(self) -> ResultE[GoProObservable[dict[SettingId, list[Any]]]]:
        """Register push notifications for all capabilities

        Returns:
            ResultE[GoProObservable[dict[SettingId, list[Any]]]]: command status and current value of all capabilities
                indexed by SettingId
        """

    ######################################################################################################
    #                          PROTOBUF COMMANDS
    ######################################################################################################

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.SET_CAMERA_CONTROL,
        response_action_id=ActionId.SET_CAMERA_CONTROL_RSP,
        request_proto=proto.RequestSetCameraControlStatus,
        response_proto=proto.ResponseGeneric,
    )
    async def set_camera_control(
        self, *, camera_control_status: proto.EnumCameraControlStatus.ValueType
    ) -> GoProResp[None]:
        """Tell the camera that the app (i.e. External Control) wishes to claim control of the camera.

        Args:
            camera_control_status (proto.EnumCameraControlStatus.ValueType): Desired camera control.

        Returns:
            GoProResp[None]: command status of request
        """

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.SET_TURBO_MODE,
        response_action_id=ActionId.SET_TURBO_MODE_RSP,
        request_proto=proto.RequestSetTurboActive,
        response_proto=proto.ResponseGeneric,
    )
    async def set_turbo_mode(self, *, mode: constants.Toggle) -> GoProResp[None]:
        """Enable / disable turbo mode.

        Args:
            mode (constants.Toggle): True to enable, False to disable.

        Returns:
            GoProResp[None]: command status of request
        """
        return {"active": mode}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_QUERY,
        feature_id=FeatureId.QUERY,
        action_id=ActionId.GET_PRESET_STATUS,
        response_action_id=ActionId.GET_PRESET_STATUS_RSP,
        request_proto=proto.RequestGetPresetStatus,
        response_proto=proto.NotifyPresetStatus,
        additional_matching_ids={ActionId.PRESET_MODIFIED_NOTIFICATION},
    )
    async def get_preset_status(
        self,
        *,
        register: list[proto.EnumRegisterPresetStatus.ValueType] | None = None,
        unregister: list[proto.EnumRegisterPresetStatus.ValueType] | None = None,
    ) -> GoProResp[proto.NotifyPresetStatus]:
        """Get information about what Preset Groups and Presets the camera supports in its current state

        Also optionally (un)register for preset / group preset modified notifications which  will be
        sent asynchronously as :py:attr:`open_gopro.models.constants.constants.ActionId.PRESET_MODIFIED_NOTIFICATION`

        Args:
            register (list[proto.EnumRegisterPresetStatus.ValueType] | None): Types of preset modified
                updates to register for. Defaults to None.
            unregister (list[proto.EnumRegisterPresetStatus.ValueType] | None): Types of preset modified
                updates to unregister for. Defaults to None.

        Returns:
            GoProResp[proto.NotifyPresetStatus]: JSON data describing all currently available presets
        """
        return {  # type: ignore
            "register_preset_status": register or [],
            "unregister_preset_status": unregister or [],
            "use_constant_setting_ids": True,
        }

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.REQUEST_PRESET_UPDATE_CUSTOM,
        response_action_id=ActionId.RESPONSE_PRESET_UPDATE_CUSTOM,
        request_proto=proto.RequestCustomPresetUpdate,
        response_proto=proto.ResponseGeneric,
    )
    async def custom_preset_update(
        self,
        icon_id: proto.EnumPresetIcon.ValueType | None = None,
        title: str | proto.EnumPresetTitle.ValueType | None = None,
    ) -> GoProResp[proto.ResponseGeneric]:
        """Update a custom preset title and / or icon

        Args:
            icon_id (proto.EnumPresetIcon.ValueType | None): Icon ID. Defaults to None.
            title (str | proto.EnumPresetTitle.ValueType | None): Custom Preset name or Factory Title ID. Defaults to None.

        Raises:
            ValueError: Did not set a parameter
            TypeError: Title was not proto.EnumPresetTitle.ValueType or string

        Returns:
            GoProResp[proto.ResponseGeneric]: status of preset update
        """
        if icon_id is None and title is None:
            raise ValueError("One of the parameters must be set")
        d: dict[Any, Any] = {}
        if icon_id:
            d["icon_id"] = icon_id
        if title is not None:
            if isinstance(title, str):
                d["title_id"] = proto.EnumPresetTitle.PRESET_TITLE_USER_DEFINED_CUSTOM_NAME
                d["custom_name"] = title
            elif isinstance(title, proto.EnumPresetTitle.ValueType):
                d["title_id"] = title
            else:
                raise TypeError("Title must be either int or str")
        return d  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_QUERY,
        feature_id=FeatureId.QUERY,
        action_id=ActionId.REQUEST_GET_LAST_MEDIA,
        response_action_id=ActionId.RESPONSE_GET_LAST_MEDIA,
        request_proto=proto.RequestGetLastCapturedMedia,
        response_proto=proto.ResponseLastCapturedMedia,
    )
    async def get_last_captured_media(self) -> GoProResp[proto.ResponseLastCapturedMedia]:
        """Get the last captured media file

        Returns:
            GoProResp[proto.ResponseLastCapturedMedia]: status of request and last captured file if successful
        """

    @ble_proto_command(
        uuid=GoProUUID.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.SCAN_WIFI_NETWORKS,
        response_action_id=ActionId.SCAN_WIFI_NETWORKS_RSP,
        request_proto=proto.RequestStartScan,
        response_proto=proto.ResponseStartScanning,
    )
    async def scan_wifi_networks(self) -> GoProResp[proto.ResponseStartScanning]:
        """Scan for Wifi networks

        Returns:
            GoProResp[proto.ResponseStartScanning]: Command status of request
        """

    @ble_proto_command(
        uuid=GoProUUID.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.GET_AP_ENTRIES,
        response_action_id=ActionId.GET_AP_ENTRIES_RSP,
        request_proto=proto.RequestGetApEntries,
        response_proto=proto.ResponseGetApEntries,
    )
    async def get_ap_entries(
        self, *, scan_id: int, start_index: int = 0, max_entries: int = 100
    ) -> GoProResp[proto.ResponseGetApEntries]:
        """Get the results of a scan for wifi networks

        Args:
            scan_id (int): ID corresponding to a set of scan results
            start_index (int): Used for paging. 0 <= start_index < NotifStartScanning.total_entries. Defaults to 0.
            max_entries (int): Used for paging. Value must be < NotifStartScanning.total_entries. Defaults to 100.

        Returns:
            GoProResp[proto.ResponseGetApEntries]: result of scan with entries for WiFi networks
        """
        return {"scan_id": scan_id, "start_index": start_index, "max_entries": max_entries}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.REQUEST_WIFI_CONNECT,
        response_action_id=ActionId.REQUEST_WIFI_CONNECT_RSP,
        request_proto=proto.RequestConnect,
        response_proto=proto.ResponseConnect,
        additional_matching_ids={ActionId.REQUEST_WIFI_CONNECT_RSP},
    )
    async def request_wifi_connect(self, *, ssid: str) -> GoProResp[proto.ResponseConnect]:
        """Request the camera to connect to a WiFi network that is already provisioned.

        Updates will be sent as :py:attr:`open_gopro.models.constants.constants.ActionId.NOTIF_PROVIS_STATE`

        Args:
            ssid (str): SSID to connect to

        Returns:
            GoProResp[proto.ResponseConnect]: Command status of request
        """

    @ble_proto_command(
        uuid=GoProUUID.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.REQUEST_WIFI_CONNECT_NEW,
        response_action_id=ActionId.REQUEST_WIFI_CONNECT_NEW_RSP,
        request_proto=proto.RequestConnectNew,
        response_proto=proto.ResponseConnectNew,
        additional_matching_ids={ActionId.REQUEST_WIFI_CONNECT_NEW_RSP},
    )
    async def request_wifi_connect_new(self, *, ssid: str, password: str) -> GoProResp[proto.ResponseConnectNew]:
        """Request the camera to connect to a WiFi network that is not already provisioned.

        Updates will be sent as :py:attr:`open_gopro.models.constants.constants.ActionId.NOTIF_PROVIS_STATE`

        Args:
            ssid (str): SSID to connect to
            password (str): password of WiFi network

        Returns:
            GoProResp[proto.ResponseConnectNew]: Command status of request
        """
        # Hard code bypass_eula_check to True.
        # On cameras where it is supported, the connection should succeed regardless of whether or not there is internet access.
        # On cameras where it is not supported, it should be ignored.
        return {  # type: ignore
            "ssid": ssid,
            "password": password,
            "bypass_eula_check": True,
        }

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.SET_LIVESTREAM_MODE,
        response_action_id=ActionId.SET_LIVESTREAM_MODE_RSP,
        request_proto=proto.RequestSetLiveStreamMode,
        response_proto=proto.ResponseGeneric,
    )
    async def set_livestream_mode(
        self,
        *,
        url: str,
        minimum_bitrate: int,
        maximum_bitrate: int,
        starting_bitrate: int,
        encode: bool = True,
        window_size: proto.EnumWindowSize.ValueType | None = None,
        lens: proto.EnumLens.ValueType | None = None,
        certs: list[Path] | None = None,
    ) -> GoProResp[None]:
        """Initiate livestream to any site that accepts an RTMP URL and simultaneously encode to camera.

        Args:
            url (str): url used to stream. Set to empty string to invalidate/cancel stream
            minimum_bitrate (int): Desired minimum streaming bitrate (>= 800)
            maximum_bitrate (int): Desired maximum streaming bitrate (<= 8000)
            starting_bitrate (int): Initial streaming bitrate (honored if 800 <= value <= 8000)
            encode (bool): Whether to save media to sdcard while streaming. Defaults to True.
            window_size (proto.EnumWindowSize.ValueType | None): Streaming video resolution. Defaults to None (use camera default).
            lens (proto.EnumLens.ValueType | None): Streaming Field of View. Defaults to None (use camera default).
            certs (list[Path] | None): list of certificates to use. Defaults to None.

        Returns:
            GoProResp[None]: command status of request
        """
        d = {
            "url": url,
            "encode": encode,
            "minimum_bitrate": minimum_bitrate,
            "maximum_bitrate": maximum_bitrate,
            "starting_bitrate": starting_bitrate,
        }
        if certs:
            cert_buf = bytearray()
            for cert in certs:
                with open(cert, "rb") as fp:
                    cert_buf += bytearray(fp.read()) + "\n".encode()

            cert_buf.pop()
            d["cert"] = bytes(cert_buf)
        if lens:
            d["lens"] = lens
        if window_size:
            d["window_size"] = window_size
        return d  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_QUERY,
        feature_id=FeatureId.QUERY,
        action_id=ActionId.GET_LIVESTREAM_STATUS,
        response_action_id=ActionId.LIVESTREAM_STATUS_RSP,
        request_proto=proto.RequestGetLiveStreamStatus,
        response_proto=proto.NotifyLiveStreamStatus,
        additional_matching_ids={ActionId.LIVESTREAM_STATUS_NOTIF},
    )
    async def register_livestream_status(
        self,
        *,
        register: list[proto.EnumRegisterLiveStreamStatus.ValueType] | None = None,
        unregister: list[proto.EnumRegisterLiveStreamStatus.ValueType] | None = None,
    ) -> GoProResp[proto.NotifyLiveStreamStatus]:
        """Register / unregister to receive asynchronous livestream statuses

        Args:
            register (list[proto.EnumRegisterLiveStreamStatus.ValueType] | None): Statuses to register
                for. Defaults to None (don't register for any).
            unregister (list[proto.EnumRegisterLiveStreamStatus.ValueType] | None): Statuses to
                unregister for. Defaults to None (don't unregister for any).

        Returns:
            GoProResp[proto.NotifyLiveStreamStatus]: current livestream status
        """
        return {"register_live_stream_status": register or [], "unregister_live_stream_status": unregister or []}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.RELEASE_NETWORK,
        response_action_id=ActionId.RELEASE_NETWORK_RSP,
        request_proto=proto.RequestReleaseNetwork,
        response_proto=proto.ResponseGeneric,
    )
    async def release_network(self) -> GoProResp[None]:
        """Disconnect the camera Wifi network in STA mode so that it returns to AP mode.

        Returns:
            GoProResp[None]: status of release request
        """

    @ble_proto_command(
        uuid=GoProUUID.CQ_QUERY,
        feature_id=FeatureId.QUERY,
        action_id=ActionId.REQUEST_GET_COHN_STATUS,
        response_action_id=ActionId.RESPONSE_GET_COHN_STATUS,
        request_proto=proto.RequestGetCOHNStatus,
        response_proto=proto.NotifyCOHNStatus,
    )
    async def cohn_get_status(self, *, register: bool) -> GoProResp[proto.NotifyCOHNStatus]:
        """Get (and optionally register for) the current COHN status

        Args:
            register (bool): whether or not to register

        Returns:
            GoProResp[proto.NotifyCOHNStatus]: current COHN status
        """
        return {"register_cohn_status": int(register)}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.REQUEST_CREATE_COHN_CERT,
        response_action_id=ActionId.RESPONSE_CREATE_COHN_CERT,
        request_proto=proto.RequestCreateCOHNCert,
        response_proto=proto.ResponseGeneric,
    )
    async def cohn_create_certificate(self, *, override: bool = False) -> GoProResp[None]:
        """Create an SSL certificate on the camera to use for COHN

        Args:
            override (bool): Should the current cert be overwritten?. Defaults to True.

        Returns:
            GoProResp[None]: certificate creation status
        """
        return {"override": int(override)}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.REQUEST_CLEAR_COHN_CERT,
        response_action_id=ActionId.RESPONSE_CLEAR_COHN_CERT,
        request_proto=proto.RequestClearCOHNCert,
        response_proto=proto.ResponseGeneric,
    )
    async def cohn_clear_certificate(self) -> GoProResp[None]:
        """Clear the current SSL certificate on the camera that is used for COHN

        Returns:
            GoProResp[None]: was the clear successful?
        """

    @ble_proto_command(
        uuid=GoProUUID.CQ_QUERY,
        feature_id=FeatureId.QUERY,
        action_id=ActionId.REQUEST_GET_COHN_CERT,
        response_action_id=ActionId.RESPONSE_GET_COHN_CERT,
        request_proto=proto.RequestCOHNCert,
        response_proto=proto.ResponseCOHNCert,
    )
    async def cohn_get_certificate(self) -> GoProResp[proto.ResponseCOHNCert]:
        """Get the current SSL certificate that the camera is using for COHN.

        Returns:
            GoProResp[proto.ResponseCOHNCert]: the certificate
        """

    @ble_proto_command(
        uuid=GoProUUID.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.REQUEST_COHN_SETTING,
        response_action_id=ActionId.RESPONSE_COHN_SETTING,
        request_proto=proto.RequestSetCOHNSetting,
        response_proto=proto.ResponseGeneric,
    )
    async def cohn_set_setting(self, *, mode: constants.Toggle) -> GoProResp[None]:
        """Set a COHN specific setting.

        Args:
            mode (constants.Toggle): should camera auto connect to home network?

        Returns:
            GoProResp[None]: status of set
        """
        return {"cohn_active": mode}  # type: ignore


class BleAsyncResponses:
    """These are responses whose ID's are not associated with any messages"""

    generic_parser: Final = Parser[bytes](
        byte_json_adapter=ConstructByteParserBuilder(Struct("unparsed" / GreedyBytes))
    )

    responses: list[BleAsyncResponse] = [
        BleAsyncResponse(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.NOTIF_PROVIS_STATE,
            Parser(byte_json_adapter=ProtobufByteParser(proto.NotifProvisioningState)),
        ),
        BleAsyncResponse(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.NOTIF_START_SCAN,
            Parser(byte_json_adapter=ProtobufByteParser(proto.NotifStartScanning)),
        ),
        BleAsyncResponse(
            FeatureId.QUERY,
            ActionId.INTERNAL_FF,
            generic_parser,
        ),
    ]

    @classmethod
    def add_parsers(cls) -> None:
        """Add all of the defined asynchronous responses to the global parser map"""
        for response in cls.responses:
            GlobalParsers.add(response.action_id, response.parser)
            GlobalParsers.add_feature_action_id_mapping(response.feature_id, response.action_id)
