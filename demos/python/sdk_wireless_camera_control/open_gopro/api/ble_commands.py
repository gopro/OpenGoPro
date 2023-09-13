# ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""BLE API for Open GoPro"""

# mypy: disable-error-code=empty-body

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Any, Final

from construct import (
    Flag,
    GreedyBytes,
    GreedyString,
    Hex,
    Int8ub,
    Int16ub,
    Int32ub,
    Int64ub,
    PaddedString,
    Padding,
    Struct,
    this,
)

from open_gopro import proto, types
from open_gopro.api.builders import (
    BleAsyncResponse,
    BleSetting,
    BleStatus,
    RegisterUnregisterAll,
    ble_proto_command,
    ble_read_command,
    ble_register_command,
    ble_write_command,
)
from open_gopro.api.parsers import ByteParserBuilders, JsonParsers
from open_gopro.communicator_interface import (
    BleMessage,
    BleMessages,
    GoProBle,
    MessageRules,
)
from open_gopro.constants import (
    ActionId,
    CmdId,
    FeatureId,
    GoProUUIDs,
    QueryCmdId,
    SettingId,
    StatusId,
)
from open_gopro.models import CameraInfo, TzDstDateTime
from open_gopro.models.response import GlobalParsers, GoProResp
from open_gopro.parser_interface import Parser
from open_gopro.types import CameraState

from . import params as Params

logger = logging.getLogger(__name__)


class BleCommands(BleMessages[BleMessage, CmdId]):
    """All of the BLE commands.

    To be used as a delegate for a GoProBle instance to build commands
    """

    ######################################################################################################
    #                          BLE WRITE COMMANDS
    ######################################################################################################

    @ble_write_command(
        uuid=GoProUUIDs.CQ_COMMAND,
        cmd=CmdId.SET_SHUTTER,
        param_builder=Int8ub,
        rules={
            MessageRules.FASTPASS: lambda **kwargs: kwargs["shutter"] == Params.Toggle.DISABLE,
            MessageRules.WAIT_FOR_ENCODING_START: lambda **kwargs: kwargs["shutter"] == Params.Toggle.ENABLE,
        },
    )
    async def set_shutter(self, *, shutter: Params.Toggle) -> GoProResp[None]:
        """Set the Shutter to start / stop encoding

        Args:
            shutter (open_gopro.api.params.Toggle): on or off

        Returns:
            GoProResp: status of command
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.TAG_HILIGHT)
    async def tag_hilight(self) -> GoProResp[None]:
        """Tag a highlight during encoding

        Returns:
            GoProResp: status of command
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.POWER_DOWN)
    async def power_down(self) -> GoProResp[None]:
        """Power Down the camera

        Returns:
            GoProResp: status of command
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.SLEEP)
    async def sleep(self) -> GoProResp[None]:
        """Put the camera in standby

        Returns:
            GoProResp: status of command
        """

    @ble_write_command(
        uuid=GoProUUIDs.CQ_COMMAND,
        cmd=CmdId.GET_HW_INFO,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.Construct(
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
            json_parser=JsonParsers.PydanticAdapter(CameraInfo),
        ),
    )
    async def get_hardware_info(self) -> GoProResp[CameraInfo]:
        """Get the model number, board, type, firmware version, serial number, and AP info

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.SET_WIFI, Int8ub)
    async def enable_wifi_ap(self, *, enable: bool) -> GoProResp[None]:
        """Enable / disable the Wi-Fi Access Point.

        Args:
            enable (bool): True to enable, False to disable

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET_GROUP, Int16ub)
    async def load_preset_group(self, *, group: proto.EnumPresetGroup) -> GoProResp[None]:
        """Load a Preset Group.

        Once complete, the most recently used preset in this group will be active.

        Args:
            group (open_gopro.api.proto.EnumPresetGroup): preset group to load

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET, Int32ub)
    async def load_preset(self, *, preset: int) -> GoProResp[None]:
        """Load a Preset

        The integer preset value can be found from the get_preset_status command

        Args:
            preset (int): preset ID to load

        Returns:
            GoProResp: command status
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.SET_THIRD_PARTY_CLIENT_INFO)
    async def set_third_party_client_info(self) -> GoProResp[None]:
        """Flag as third party app

        Returns:
            GoProResp: command status
        """

    @ble_write_command(
        uuid=GoProUUIDs.CQ_COMMAND,
        cmd=CmdId.GET_THIRD_PARTY_API_VERSION,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.Construct(
                Struct(Padding(1), "major" / Int8ub, Padding(1), "minor" / Int8ub)
            ),
            json_parser=JsonParsers.LambdaParser(lambda data: f"{data['major']}.{data['minor']}"),
        ),
    )
    async def get_open_gopro_api_version(self) -> GoProResp[str]:
        """Get Open GoPro API Version

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.GET_CAMERA_STATUSES,
        parser=Parser(json_parser=JsonParsers.CameraStateParser()),
    )
    async def get_camera_statuses(self) -> GoProResp[CameraState]:
        """Get all of the camera's statuses

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.GET_CAMERA_SETTINGS,
        parser=Parser(json_parser=JsonParsers.CameraStateParser()),
    )
    async def get_camera_settings(self) -> GoProResp[CameraState]:
        """Get all of the camera's settings

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.GET_CAMERA_CAPABILITIES,
        parser=Parser(json_parser=JsonParsers.CameraStateParser()),
    )
    async def get_camera_capabilities(self) -> GoProResp[CameraState]:
        """Get the current capabilities of each camera setting

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.SET_DATE_TIME, param_builder=ByteParserBuilders.DateTime())
    async def set_date_time(self, *, date_time: datetime.datetime) -> GoProResp[None]:
        """Set the camera's date and time (non timezone / DST version)

        Args:
            date_time (datetime.datetime): Date and time to set (Timezone will be ignored)

        Returns:
            GoProResp: command status
        """

    @ble_write_command(
        GoProUUIDs.CQ_COMMAND,
        CmdId.GET_DATE_TIME,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.DateTime(),
            json_parser=JsonParsers.LambdaParser(lambda data: data["datetime"]),
        ),
    )
    async def get_date_time(self) -> GoProResp[datetime.datetime]:
        """Get the camera's date and time (non timezone / DST version)

        Returns:
            GoProResp: response as JSON
        """

    @ble_write_command(GoProUUIDs.CQ_COMMAND, CmdId.SET_DATE_TIME_DST, param_builder=ByteParserBuilders.DateTime())
    async def set_date_time_tz_dst(
        self, *, date_time: datetime.datetime, tz_offset: int, is_dst: bool
    ) -> GoProResp[None]:
        """Set the camera's date and time with timezone and DST

        Args:
            date_time (datetime.datetime): date and time
            tz_offset (int): timezone as UTC offset
            is_dst (bool): is daylight savings time?

        Returns:
            GoProResp: command status
        """

    @ble_write_command(
        GoProUUIDs.CQ_COMMAND,
        CmdId.GET_DATE_TIME_DST,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.DateTime(),
            json_parser=JsonParsers.PydanticAdapter(TzDstDateTime),
        ),
    )
    async def get_date_time_tz_dst(self) -> GoProResp[TzDstDateTime]:
        """Get the camera's date and time with timezone / DST

        Returns:
            GoProResp: response as JSON
        """

    ######################################################################################################
    #                          BLE DIRECT CHARACTERISTIC READ COMMANDS
    ######################################################################################################

    @ble_read_command(
        uuid=GoProUUIDs.WAP_SSID,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.Construct(Struct("ssid" / GreedyString("utf-8"))),
            json_parser=JsonParsers.LambdaParser(lambda data: data["ssid"]),
        ),
    )
    async def get_wifi_ssid(self) -> GoProResp[str]:
        """Get the Wifi SSID.

        Returns:
            GoProResp: command status and SSID
        """

    @ble_read_command(
        uuid=GoProUUIDs.WAP_PASSWORD,
        parser=Parser(
            byte_json_adapter=ByteParserBuilders.Construct(Struct("password" / GreedyString("utf-8"))),
            json_parser=JsonParsers.LambdaParser(lambda data: data["password"]),
        ),
    )
    async def get_wifi_password(self) -> GoProResp[str]:
        """Get the Wifi password.

        Returns:
            GoProResp: command status and password
        """

    ######################################################################################################
    #                          REGISTER / UNREGISTER ALL COMMANDS
    ######################################################################################################

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.REGISTER_ALL_STATUSES,
        update_set=StatusId,
        responded_cmd=QueryCmdId.STATUS_VAL_PUSH,  # TODO probably remove this
        action=RegisterUnregisterAll.Action.REGISTER,
    )
    async def register_for_all_statuses(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register push notifications for all statuses

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status and current value of all statuses
        """

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.UNREGISTER_ALL_STATUSES,
        update_set=StatusId,
        responded_cmd=QueryCmdId.STATUS_VAL_PUSH,
        action=RegisterUnregisterAll.Action.UNREGISTER,
    )
    async def unregister_for_all_statuses(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Unregister push notifications for all statuses

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status
        """

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.REGISTER_ALL_SETTINGS,
        update_set=SettingId,
        responded_cmd=QueryCmdId.SETTING_VAL_PUSH,
        action=RegisterUnregisterAll.Action.REGISTER,
    )
    async def register_for_all_settings(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register push notifications for all settings

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status and current value of all settings
        """

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.UNREGISTER_ALL_SETTINGS,
        update_set=SettingId,
        responded_cmd=QueryCmdId.SETTING_VAL_PUSH,
        action=RegisterUnregisterAll.Action.UNREGISTER,
    )
    async def unregister_for_all_settings(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Unregister push notifications for all settings

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status
        """

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.REGISTER_ALL_CAPABILITIES,
        update_set=SettingId,
        responded_cmd=QueryCmdId.SETTING_CAPABILITY_PUSH,
        action=RegisterUnregisterAll.Action.REGISTER,
    )
    async def register_for_all_capabilities(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register push notifications for all capabilities

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status and current value of all capabilities
        """

    @ble_register_command(
        GoProUUIDs.CQ_QUERY,
        CmdId.UNREGISTER_ALL_CAPABILITIES,
        update_set=SettingId,
        responded_cmd=QueryCmdId.SETTING_CAPABILITY_PUSH,
        action=RegisterUnregisterAll.Action.UNREGISTER,
    )
    async def unregister_for_all_capabilities(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Unregister push notifications for all capabilities

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: command status
        """

    ######################################################################################################
    #                          PROTOBUF COMMANDS
    ######################################################################################################

    @ble_proto_command(
        uuid=GoProUUIDs.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.SET_CAMERA_CONTROL,
        response_action_id=ActionId.SET_CAMERA_CONTROL_RSP,
        request_proto=proto.RequestSetCameraControlStatus,
        response_proto=proto.ResponseGeneric,
    )
    async def set_camera_control(self, *, camera_control_status: proto.EnumCameraControlStatus) -> GoProResp[None]:
        """Tell the camera that the app (i.e. External Control) wishes to claim control of the camera.

        Args:
            camera_control_status (open_gopro.api.proto.EnumCameraControlStatus): Desired camera control.

        Returns:
            GoProResp: command status of request
        """

    @ble_proto_command(
        uuid=GoProUUIDs.CQ_COMMAND,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.SET_TURBO_MODE,
        response_action_id=ActionId.SET_TURBO_MODE_RSP,
        request_proto=proto.RequestSetTurboActive,
        response_proto=proto.ResponseGeneric,
    )
    async def set_turbo_mode(self, *, mode: Params.Toggle) -> GoProResp[None]:
        """Enable / disable turbo mode.

        Args:
            mode (open_gopro.api.params.Toggle): True to enable, False to disable.

        Returns:
            GoProResp: command status of request
        """
        return {"active": mode}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUIDs.CQ_QUERY,
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
        register: list[proto.EnumRegisterPresetStatus] | None = None,
        unregister: list[proto.EnumRegisterPresetStatus] | None = None,
    ) -> GoProResp[proto.NotifyPresetStatus]:
        """Get information about what Preset Groups and Presets the camera supports in its current state

        Also optionally (un)register for preset / group preset modified notifications which  will be
        sent asynchronously as :py:attr:`open_gopro.constants.ActionId.PRESET_MODIFIED_NOTIFICATION`

        Args:
            register (list[open_gopro.api.proto.EnumRegisterPresetStatus], Optional): Types of preset modified
                updates to register for. Defaults to None.
            unregister (list[open_gopro.api.proto.EnumRegisterPresetStatus], Optional): Types of preset modified
                updates to unregister for. Defaults to None.

        Returns:
            GoProResp: JSON data describing all currently available presets
        """
        return {  # type: ignore
            "register_preset_status": register or [],
            "unregister_preset_status": unregister or [],
        }

    @ble_proto_command(
        uuid=GoProUUIDs.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.SCAN_WIFI_NETWORKS,
        response_action_id=ActionId.SCAN_WIFI_NETWORKS_RSP,
        request_proto=proto.RequestStartScan,
        response_proto=proto.ResponseStartScanning,
    )
    async def scan_wifi_networks(self) -> GoProResp[proto.ResponseStartScanning]:
        """Scan for Wifi networks

        Returns:
            GoProResp: Command status of request
        """

    @ble_proto_command(
        uuid=GoProUUIDs.CM_NET_MGMT_COMM,
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
            GoProResp: result of scan with entries for WiFi networks
        """
        return {"scan_id": scan_id, "start_index": start_index, "max_entries": max_entries}  # type: ignore

    @ble_proto_command(
        uuid=GoProUUIDs.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.REQUEST_WIFI_CONNECT,
        response_action_id=ActionId.REQUEST_WIFI_CONNECT_RSP,
        request_proto=proto.RequestConnect,
        response_proto=proto.ResponseConnect,
        additional_matching_ids={ActionId.REQUEST_WIFI_CONNECT_RSP},
    )
    async def request_wifi_connect(self, *, ssid: str) -> GoProResp[proto.ResponseConnect]:
        """Request the camera to connect to a WiFi network that is already provisioned.

        Updates will be sent as :py:attr:`open_gopro.constants.ActionId.NOTIF_PROVIS_STATE`

        Args:
            ssid (str): SSID to connect to

        Returns:
            GoProResp: Command status of request
        """

    @ble_proto_command(
        uuid=GoProUUIDs.CM_NET_MGMT_COMM,
        feature_id=FeatureId.NETWORK_MANAGEMENT,
        action_id=ActionId.REQUEST_WIFI_CONNECT_NEW,
        response_action_id=ActionId.REQUEST_WIFI_CONNECT_NEW_RSP,
        request_proto=proto.RequestConnectNew,
        response_proto=proto.ResponseConnectNew,
        additional_matching_ids={ActionId.REQUEST_WIFI_CONNECT_NEW_RSP},
    )
    async def request_wifi_connect_new(self, *, ssid: str, password: str) -> GoProResp[proto.ResponseConnectNew]:
        """Request the camera to connect to a WiFi network that is not already provisioned.

        Updates will be sent as :py:attr:`open_gopro.constants.ActionId.NOTIF_PROVIS_STATE`

        Args:
            ssid (str): SSID to connect to
            password (str): password of WiFi network

        Returns:
            GoProResp: Command status of request
        """

    @ble_proto_command(
        uuid=GoProUUIDs.CQ_COMMAND,
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
        window_size: proto.EnumWindowSize,
        minimum_bitrate: int,
        maximum_bitrate: int,
        starting_bitrate: int,
        lens: proto.EnumLens,
        certs: list[Path] | None = None,
    ) -> GoProResp[None]:
        """Initiate livestream to any site that accepts an RTMP URL and simultaneously encode to camera.

        Args:
            url (str): url used to stream. Set to empty string to invalidate/cancel stream
            window_size (open_gopro.api.proto.EnumWindowSize): Streaming video resolution
            minimum_bitrate (int): Desired minimum streaming bitrate (>= 800)
            maximum_bitrate (int): Desired maximum streaming bitrate (<= 8000)
            starting_bitrate (int): Initial streaming bitrate (honored if 800 <= value <= 8000)
            lens (open_gopro.api.proto.EnumLens): Streaming Field of View
            certs (list[Path] | None): list of certificates to use. Defaults to None.

        Returns:
            GoProResp: command status of request
        """
        d = {
            "url": url,
            "encode": True,
            "window_size": window_size,
            "minimum_bitrate": minimum_bitrate,
            "maximum_bitrate": maximum_bitrate,
            "starting_bitrate": starting_bitrate,
            "lens": lens,
        }
        if certs:
            cert_buf = bytearray()
            for cert in certs:
                with open(cert, "rb") as fp:
                    cert_buf += bytearray(fp.read()) + "\n".encode()

            cert_buf.pop()
            d["cert"] = bytes(cert_buf)
        return d  # type: ignore

    @ble_proto_command(
        uuid=GoProUUIDs.CQ_QUERY,
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
        register: list[proto.EnumRegisterLiveStreamStatus] | None = None,
        unregister: list[proto.EnumRegisterLiveStreamStatus] | None = None,
    ) -> GoProResp[proto.NotifyLiveStreamStatus]:
        """Register / unregister to receive asynchronous livestream statuses

        Args:
            register (Optional[list[open_gopro.api.proto.EnumRegisterLiveStreamStatus]]): Statuses to register
                for. Defaults to None (don't register for any).
            unregister (Optional[list[open_gopro.api.proto.EnumRegisterLiveStreamStatus]]): Statues to
                unregister for. Defaults to None (don't unregister for any).

        Returns:
            GoProResp: current livestream status
        """
        return {"register_live_stream_status": register or [], "unregister_live_stream_status": unregister or []}  # type: ignore


class BleSettings(BleMessages[BleSetting, SettingId]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all BLE Settings.

    To be used by a GoProBle delegate to build setting messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (type[Params]): the set of parameters to use to build the settings
    """

    def __init__(self, communicator: GoProBle):

        self.resolution: BleSetting[Params.Resolution] = BleSetting[Params.Resolution](
            communicator, SettingId.RESOLUTION, Params.Resolution
        )
        """Resolution."""

        self.fps: BleSetting[Params.FPS] = BleSetting[Params.FPS](communicator, SettingId.FPS, Params.FPS)
        """Frames per second."""

        self.auto_off: BleSetting[Params.AutoOff] = BleSetting[Params.AutoOff](
            communicator, SettingId.AUTO_OFF, Params.AutoOff
        )
        """Set the auto off time."""

        self.video_field_of_view: BleSetting[Params.VideoFOV] = BleSetting[Params.VideoFOV](
            communicator, SettingId.VIDEO_FOV, Params.VideoFOV
        )
        """Video FOV."""

        self.photo_field_of_view: BleSetting[Params.PhotoFOV] = BleSetting[Params.PhotoFOV](
            communicator, SettingId.PHOTO_FOV, Params.PhotoFOV
        )
        """Photo FOV."""

        self.multi_shot_field_of_view: BleSetting[Params.MultishotFOV] = BleSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV, Params.MultishotFOV
        )
        """Multi-shot FOV."""

        self.led: BleSetting[Params.LED] = BleSetting[Params.LED](communicator, SettingId.LED, Params.LED)
        """Set the LED options (or also send the BLE keep alive signal)."""

        self.max_lens_mode: BleSetting[Params.MaxLensMode] = BleSetting[Params.MaxLensMode](
            communicator, SettingId.MAX_LENS_MOD, Params.MaxLensMode
        )
        """Enable / disable max lens mod."""

        self.hypersmooth: BleSetting[Params.HypersmoothMode] = BleSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH, Params.HypersmoothMode
        )
        """Set / disable hypersmooth."""

        self.video_performance_mode: BleSetting[Params.PerformanceMode] = BleSetting[Params.PerformanceMode](
            communicator,
            SettingId.VIDEO_PERFORMANCE_MODE,
            Params.PerformanceMode,
        )
        """Video Performance Mode."""

        self.media_format: BleSetting[Params.MediaFormat] = BleSetting[Params.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT, Params.MediaFormat
        )
        """Set the media format."""

        self.anti_flicker: BleSetting[Params.AntiFlicker] = BleSetting[Params.AntiFlicker](
            communicator,
            SettingId.ANTI_FLICKER,
            Params.AntiFlicker,
        )
        """Anti Flicker frequency."""

        self.camera_ux_mode: BleSetting[Params.CameraUxMode] = BleSetting[Params.CameraUxMode](
            communicator,
            SettingId.CAMERA_UX_MODE,
            Params.CameraUxMode,
        )
        """Camera controls configuration."""

        self.video_easy_mode: BleSetting[Params.Speed] = BleSetting[Params.Speed](
            communicator,
            SettingId.VIDEO_EASY_MODE,
            Params.Speed,
        )
        """Video easy mode speed."""

        self.photo_easy_mode: BleSetting[Params.PhotoEasyMode] = BleSetting[Params.PhotoEasyMode](
            communicator,
            SettingId.PHOTO_EASY_MODE,
            Params.PhotoEasyMode,
        )
        """Night Photo easy mode."""

        self.wifi_band: BleSetting[Params.WifiBand] = BleSetting[Params.WifiBand](
            communicator,
            SettingId.WIFI_BAND,
            Params.WifiBand,
        )
        """Current WiFi band being used."""

        self.star_trail_length: BleSetting[Params.StarTrailLength] = BleSetting[Params.StarTrailLength](
            communicator,
            SettingId.STAR_TRAIL_LENGTH,
            Params.StarTrailLength,
        )
        """Multi shot star trail length."""

        self.system_video_mode: BleSetting[Params.SystemVideoMode] = BleSetting[Params.SystemVideoMode](
            communicator,
            SettingId.SYSTEM_VIDEO_MODE,
            Params.SystemVideoMode,
        )
        """System video mode."""

        self.video_horizon_leveling: BleSetting[Params.HorizonLeveling] = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.VIDEO_HORIZON_LEVELING,
            Params.HorizonLeveling,
        )
        """Lock / unlock horizon leveling for video."""

        self.photo_horizon_leveling: BleSetting[Params.HorizonLeveling] = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.PHOTO_HORIZON_LEVELING,
            Params.HorizonLeveling,
        )
        """Lock / unlock horizon leveling for photo."""

        self.bit_rate: BleSetting[Params.BitRate] = BleSetting[Params.BitRate](
            communicator,
            SettingId.BIT_RATE,
            Params.BitRate,
        )
        """System Video Bit Rate."""

        self.bit_depth: BleSetting[Params.BitDepth] = BleSetting[Params.BitDepth](
            communicator,
            SettingId.BIT_DEPTH,
            Params.BitDepth,
        )
        """System Video Bit depth."""

        self.video_profile: BleSetting[Params.VideoProfile] = BleSetting[Params.VideoProfile](
            communicator,
            SettingId.VIDEO_PROFILE,
            Params.VideoProfile,
        )
        """Video Profile (hdr, etc.)"""

        self.video_aspect_ratio: BleSetting[Params.VideoAspectRatio] = BleSetting[Params.VideoAspectRatio](
            communicator,
            SettingId.VIDEO_ASPECT_RATIO,
            Params.VideoAspectRatio,
        )
        """Video aspect ratio"""

        self.video_easy_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.VIDEO_EASY_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Video easy aspect ratio"""

        self.multi_shot_easy_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_EASY_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Multi shot easy aspect ratio"""

        self.multi_shot_nlv_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_NLV_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Multi shot NLV aspect ratio"""

        self.video_mode: BleSetting[Params.VideoMode] = BleSetting[Params.VideoMode](
            communicator,
            SettingId.VIDEO_MODE,
            Params.VideoMode,
        )
        """Video Mode (i.e. quality)"""

        self.timelapse_mode: BleSetting[Params.TimelapseMode] = BleSetting[Params.TimelapseMode](
            communicator,
            SettingId.TIMELAPSE_MODE,
            Params.TimelapseMode,
        )
        """Timelapse Mode"""

        self.maxlens_mod_type: BleSetting[Params.MaxLensModType] = BleSetting[Params.MaxLensModType](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD,
            Params.MaxLensModType,
        )
        """Max lens mod? If so, what type?"""

        self.maxlens_status: BleSetting[Params.Toggle] = BleSetting[Params.Toggle](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD_ENABLE,
            Params.Toggle,
        )
        """Enable / disable max lens mod"""

        self.photo_mode: BleSetting[Params.PhotoMode] = BleSetting[Params.PhotoMode](
            communicator,
            SettingId.PHOTO_MODE,
            Params.PhotoMode,
        )
        """Photo Mode"""

        self.framing: BleSetting[Params.Framing] = BleSetting[Params.Framing](
            communicator,
            SettingId.FRAMING,
            Params.Framing,
        )
        """Video Framing Mode"""

        self.hindsight: BleSetting[Params.Hindsight] = BleSetting[Params.Hindsight](
            communicator,
            SettingId.HINDSIGHT,
            Params.Hindsight,
        )
        """Hindsight time / disable"""

        self.photo_interval: BleSetting[Params.PhotoInterval] = BleSetting[Params.PhotoInterval](
            communicator,
            SettingId.PHOTO_INTERVAL,
            Params.PhotoInterval,
        )
        """Interval between photo captures"""

        self.photo_duration: BleSetting[Params.PhotoDuration] = BleSetting[Params.PhotoDuration](
            communicator,
            SettingId.PHOTO_INTERVAL_DURATION,
            Params.PhotoDuration,
        )
        """Interval between photo captures"""

        super().__init__(communicator)


class BleAsyncResponses:
    """These are responses whose ID's are not associated with any messages"""

    generic_parser: Final = Parser[bytes](
        byte_json_adapter=ByteParserBuilders.Construct(Struct("unparsed" / GreedyBytes))
    )

    responses: list[BleAsyncResponse] = [
        BleAsyncResponse(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.NOTIF_PROVIS_STATE,
            Parser(byte_json_adapter=ByteParserBuilders.Protobuf(proto.NotifProvisioningState)),
        ),
        BleAsyncResponse(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.NOTIF_START_SCAN,
            Parser(byte_json_adapter=ByteParserBuilders.Protobuf(proto.NotifStartScanning)),
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


class BleStatuses(BleMessages[BleStatus, StatusId]):
    """All of the BLE Statuses.

    To be used by a GoProBle delegate to build status messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (type[Params]): the set of parameters to use to build the statuses
    """

    def __init__(self, communicator: GoProBle) -> None:
        self.batt_present: BleStatus[bool] = BleStatus(communicator, StatusId.BATT_PRESENT, Flag)
        """Is the system's internal battery present?"""

        self.batt_level: BleStatus[int] = BleStatus(communicator, StatusId.BATT_LEVEL, Int8ub)
        """Rough approximation of internal battery level in bars."""

        # TODO can we just not define deprecated statuses?
        self.deprecated_3: BleStatus[Any] = BleStatus(
            communicator, StatusId.DEPRECATED_3, ByteParserBuilders.DeprecatedMarker()
        )
        """This status is deprecated."""

        self.deprecated_4: BleStatus[Any] = BleStatus(
            communicator, StatusId.DEPRECATED_4, ByteParserBuilders.DeprecatedMarker()
        )
        """This status is deprecated."""

        self.system_hot: BleStatus[bool] = BleStatus(communicator, StatusId.SYSTEM_HOT, Flag)
        """Is the system currently overheating?"""

        self.system_busy: BleStatus[bool] = BleStatus(communicator, StatusId.SYSTEM_BUSY, Flag)
        """Is the camera busy?"""

        self.quick_capture: BleStatus[bool] = BleStatus(communicator, StatusId.QUICK_CAPTURE, Flag)
        """Is quick capture feature enabled?"""

        self.encoding_active: BleStatus[bool] = BleStatus(communicator, StatusId.ENCODING, Flag)
        """Is the camera currently encoding (i.e. capturing photo / video)?"""

        self.lcd_lock_active: BleStatus[bool] = BleStatus(communicator, StatusId.LCD_LOCK_ACTIVE, Flag)
        """Is the LCD lock currently active?"""

        self.video_progress: BleStatus[int] = BleStatus(communicator, StatusId.VIDEO_PROGRESS, Int32ub)
        """When encoding video, this is the duration (seconds) of the video so far; 0 otherwise."""

        self.wireless_enabled: BleStatus[bool] = BleStatus(communicator, StatusId.WIRELESS_ENABLED, Flag)
        """Are Wireless Connections enabled?"""

        self.pair_state: BleStatus[Params.PairState] = BleStatus(communicator, StatusId.PAIR_STATE, Params.PairState)
        """What is the pair state?"""

        self.pair_type: BleStatus[Params.PairType] = BleStatus(communicator, StatusId.PAIR_TYPE, Params.PairType)
        """The last type of pairing that the camera was engaged in."""

        self.pair_time: BleStatus[int] = BleStatus(communicator, StatusId.PAIR_TIME, Int32ub)
        """	Time (milliseconds) since boot of last successful pairing complete action."""

        self.wap_scan_state: BleStatus[Params.PairType] = BleStatus(
            communicator, StatusId.WAP_SCAN_STATE, Params.WAPState
        )
        """State of current scan for Wifi Access Points. Appears to only change for CAH-related scans."""

        # TODO this is returning different sized data in BLE vs WiFi
        # self.wap_scan_time:[int] BleStatus = BleStatus(communicator, StatusId.WAP_SCAN_TIME, Int8ub)
        # """The time, in milliseconds since boot that the Wifi Access Point scan completed."""

        self.wap_prov_stat: BleStatus[Params.PairType] = BleStatus(
            communicator, StatusId.WAP_PROV_STAT, Params.WAPState
        )
        """Wifi AP provisioning state."""

        self.remote_ctrl_ver: BleStatus[int] = BleStatus(communicator, StatusId.REMOTE_CTRL_VER, Int8ub)
        """What is the remote control version?"""

        self.remote_ctrl_conn: BleStatus[bool] = BleStatus(communicator, StatusId.REMOTE_CTRL_CONN, Flag)
        """Is the remote control connected?"""

        self.pair_state2: BleStatus[int] = BleStatus(communicator, StatusId.PAIR_STATE2, Int8ub)
        """Wireless Pairing State."""

        self.wlan_ssid: BleStatus[str] = BleStatus(communicator, StatusId.WLAN_SSID, GreedyString(encoding="utf-8"))
        """Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.ap_ssid: BleStatus[str] = BleStatus(communicator, StatusId.AP_SSID, GreedyString(encoding="utf-8"))
        """Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.app_count: BleStatus[int] = BleStatus(communicator, StatusId.APP_COUNT, Int8ub)
        """The number of wireless devices connected to the camera."""

        self.preview_enabled: BleStatus[bool] = BleStatus(communicator, StatusId.PREVIEW_ENABLED, Flag)
        """Is preview stream enabled?"""

        self.sd_status: BleStatus[Params.SDStatus] = BleStatus(communicator, StatusId.SD_STATUS, Params.SDStatus)
        """Primary Storage Status."""

        self.photos_rem: BleStatus[int] = BleStatus(communicator, StatusId.PHOTOS_REM, Int32ub)
        """How many photos can be taken before sdcard is full?"""

        self.video_rem: BleStatus[int] = BleStatus(communicator, StatusId.VIDEO_REM, Int32ub)
        """How many minutes of video can be captured with current settings before sdcard is full?"""

        self.num_group_photo: BleStatus[int] = BleStatus(communicator, StatusId.NUM_GROUP_PHOTO, Int32ub)
        """How many group photos can be taken with current settings before sdcard is full?"""

        self.num_group_video: BleStatus[int] = BleStatus(communicator, StatusId.NUM_GROUP_VIDEO, Int32ub)
        """Total number of group videos on sdcard."""

        self.num_total_photo: BleStatus[int] = BleStatus(communicator, StatusId.NUM_TOTAL_PHOTO, Int32ub)
        """Total number of photos on sdcard."""

        self.num_total_video: BleStatus[int] = BleStatus(communicator, StatusId.NUM_TOTAL_VIDEO, Int32ub)
        """Total number of videos on sdcard."""

        self.deprecated_40: BleStatus[Any] = BleStatus(
            communicator, StatusId.DEPRECATED_40, ByteParserBuilders.DeprecatedMarker()
        )
        """This status is deprecated."""

        self.ota_stat: BleStatus[Params.OTAStatus] = BleStatus(communicator, StatusId.OTA_STAT, Params.OTAStatus)
        """The current status of Over The Air (OTA) update."""

        self.download_cancel_pend: BleStatus[bool] = BleStatus(communicator, StatusId.DOWNLOAD_CANCEL_PEND, Flag)
        """Is download firmware update cancel request pending?"""

        self.mode_group: BleStatus[int] = BleStatus(communicator, StatusId.MODE_GROUP, Int8ub)
        """Current mode group (deprecated in HERO8)."""

        self.locate_active: BleStatus[bool] = BleStatus(communicator, StatusId.LOCATE_ACTIVE, Flag)
        """Is locate camera feature active?"""

        self.multi_count_down: BleStatus[int] = BleStatus(communicator, StatusId.MULTI_COUNT_DOWN, Int32ub)
        """The current timelapse interval countdown value (e.g. 5...4...3...2...1...)."""

        self.space_rem: BleStatus[int] = BleStatus(communicator, StatusId.SPACE_REM, Int64ub)
        """Remaining space on the sdcard in Kilobytes."""

        self.streaming_supp: BleStatus[bool] = BleStatus(communicator, StatusId.STREAMING_SUPP, Flag)
        """Is streaming supports in current recording/flatmode/secondary-stream?"""

        self.wifi_bars: BleStatus[int] = BleStatus(communicator, StatusId.WIFI_BARS, Int8ub)
        """Wifi signal strength in bars."""

        self.current_time_ms: BleStatus[int] = BleStatus(communicator, StatusId.CURRENT_TIME_MS, Int32ub)
        """System time in milliseconds since system was booted."""

        self.num_hilights: BleStatus[int] = BleStatus(communicator, StatusId.NUM_HILIGHTS, Int8ub)
        """The number of hilights in encoding video (set to 0 when encoding stops)."""

        self.last_hilight: BleStatus[int] = BleStatus(communicator, StatusId.LAST_HILIGHT, Int32ub)
        """Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)."""

        self.next_poll: BleStatus[int] = BleStatus(communicator, StatusId.NEXT_POLL, Int32ub)
        """The min time between camera status updates (msec). Do not poll for status more often than this."""

        self.analytics_rdy: BleStatus[Params.AnalyticsState] = BleStatus(
            communicator, StatusId.ANALYTICS_RDY, Params.AnalyticsState
        )
        """The current state of camera analytics."""

        self.analytics_size: BleStatus[int] = BleStatus(communicator, StatusId.ANALYTICS_SIZE, Int32ub)
        """The size (units??) of the analytics file."""

        self.in_context_menu: BleStatus[bool] = BleStatus(communicator, StatusId.IN_CONTEXT_MENU, Flag)
        """Is the camera currently in a contextual menu (e.g. Preferences)?"""

        self.timelapse_rem: BleStatus[int] = BleStatus(communicator, StatusId.TIMELAPSE_REM, Int32ub)
        """How many min of Timelapse video can be captured with current settings before sdcard is full?"""

        self.exposure_type: BleStatus[Params.ExposureMode] = BleStatus(
            communicator, StatusId.EXPOSURE_TYPE, Params.ExposureMode
        )
        """Liveview Exposure Select Mode."""

        self.exposure_x: BleStatus[int] = BleStatus(communicator, StatusId.EXPOSURE_X, Int8ub)
        """Liveview Exposure Select for y-coordinate (percent)."""

        self.exposure_y: BleStatus[int] = BleStatus(communicator, StatusId.EXPOSURE_Y, Int8ub)
        """Liveview Exposure Select for y-coordinate (percent)."""

        self.gps_stat: BleStatus[bool] = BleStatus(communicator, StatusId.GPS_STAT, Flag)
        """Does the camera currently have a GPS lock?"""

        self.ap_state: BleStatus[bool] = BleStatus(communicator, StatusId.AP_STATE, Flag)
        """Is the Wifi radio enabled?"""

        self.int_batt_per: BleStatus[int] = BleStatus(communicator, StatusId.INT_BATT_PER, Int8ub)
        """Internal battery level (percent)."""

        self.acc_mic_stat: BleStatus[Params.ExposureMode] = BleStatus(
            communicator, StatusId.ACC_MIC_STAT, Params.ExposureMode
        )
        """Microphone Accessory status."""

        self.digital_zoom: BleStatus[int] = BleStatus(communicator, StatusId.DIGITAL_ZOOM, Int8ub)
        """	Digital Zoom level (percent)."""

        self.wireless_band: BleStatus[Params.WifiBand] = BleStatus(
            communicator, StatusId.WIRELESS_BAND, Params.WifiBand
        )
        """Wireless Band."""

        self.dig_zoom_active: BleStatus[bool] = BleStatus(communicator, StatusId.DIG_ZOOM_ACTIVE, Flag)
        """Is Digital Zoom feature available?"""

        self.mobile_video: BleStatus[bool] = BleStatus(communicator, StatusId.MOBILE_VIDEO, Flag)
        """Are current video settings mobile friendly? (related to video compression and frame rate)."""

        self.first_time: BleStatus[bool] = BleStatus(communicator, StatusId.FIRST_TIME, Flag)
        """Is the camera currently in First Time Use (FTU) UI flow?"""

        self.sec_sd_stat: BleStatus[Params.SDStatus] = BleStatus(communicator, StatusId.SEC_SD_STAT, Params.SDStatus)
        """Secondary Storage Status (exclusive to Superbank)."""

        self.band_5ghz_avail: BleStatus[bool] = BleStatus(communicator, StatusId.BAND_5GHZ_AVAIL, Flag)
        """Is 5GHz wireless band available?"""

        self.system_ready: BleStatus[bool] = BleStatus(communicator, StatusId.SYSTEM_READY, Flag)
        """Is the system ready to accept messages?"""

        self.batt_ok_ota: BleStatus[bool] = BleStatus(communicator, StatusId.BATT_OK_OTA, Flag)
        """Is the internal battery charged sufficiently to start Over The Air (OTA) update?"""

        self.video_low_temp: BleStatus[bool] = BleStatus(communicator, StatusId.VIDEO_LOW_TEMP, Flag)
        """Is the camera getting too cold to continue recording?"""

        self.orientation: BleStatus[Params.Orientation] = BleStatus(
            communicator, StatusId.ORIENTATION, Params.Orientation
        )
        """The rotational orientation of the camera."""

        self.deprecated_87: BleStatus[Any] = BleStatus(
            communicator, StatusId.DEPRECATED_87, ByteParserBuilders.DeprecatedMarker()
        )
        """This status is deprecated."""

        self.zoom_encoding: BleStatus[bool] = BleStatus(communicator, StatusId.ZOOM_ENCODING, Flag)
        """Is this camera capable of zooming while encoding (static value based on model, not settings)?"""

        self.flatmode_id: BleStatus[Params.Flatmode] = BleStatus(communicator, StatusId.FLATMODE_ID, Params.Flatmode)
        """Current flatmode ID."""

        self.logs_ready: BleStatus[bool] = BleStatus(communicator, StatusId.LOGS_READY, Flag)
        """	Are system logs ready to be downloaded?"""

        self.deprecated_92: BleStatus[Any] = BleStatus(
            communicator, StatusId.DEPRECATED_92, ByteParserBuilders.DeprecatedMarker()
        )
        """This status is deprecated."""

        self.video_presets: BleStatus[int] = BleStatus(communicator, StatusId.VIDEO_PRESETS, Int32ub)
        """Current Video Preset (ID)."""

        self.photo_presets: BleStatus[int] = BleStatus(communicator, StatusId.PHOTO_PRESETS, Int32ub)
        """Current Photo Preset (ID)."""

        self.timelapse_presets: BleStatus[int] = BleStatus(communicator, StatusId.TIMELAPSE_PRESETS, Int32ub)
        """	Current Timelapse Preset (ID)."""

        self.presets_group: BleStatus[int] = BleStatus(communicator, StatusId.PRESETS_GROUP, Int32ub)
        """Current Preset Group (ID)."""

        self.active_preset: BleStatus[int] = BleStatus(communicator, StatusId.ACTIVE_PRESET, Int32ub)
        """Currently Preset (ID)."""

        self.preset_modified: BleStatus[int] = BleStatus(communicator, StatusId.PRESET_MODIFIED, Int32ub)
        """Preset Modified Status, which contains an event ID and a preset (group) ID."""

        self.live_burst_rem: BleStatus[int] = BleStatus(communicator, StatusId.LIVE_BURST_REM, Int32ub)
        """How many Live Bursts can be captured before sdcard is full?"""

        self.live_burst_total: BleStatus[int] = BleStatus(communicator, StatusId.LIVE_BURST_TOTAL, Int32ub)
        """Total number of Live Bursts on sdcard."""

        self.capt_delay_active: BleStatus[bool] = BleStatus(communicator, StatusId.CAPT_DELAY_ACTIVE, Flag)
        """Is Capture Delay currently active (i.e. counting down)?"""

        self.media_mod_mic_stat: BleStatus[Params.MediaModMicStatus] = BleStatus(
            communicator, StatusId.MEDIA_MOD_MIC_STAT, Params.MediaModMicStatus
        )
        """Media mod State."""

        self.timewarp_speed_ramp: BleStatus[Params.TimeWarpSpeed] = BleStatus(
            communicator, StatusId.TIMEWARP_SPEED_RAMP, Params.TimeWarpSpeed
        )
        """Time Warp Speed."""

        self.linux_core_active: BleStatus[bool] = BleStatus(communicator, StatusId.LINUX_CORE_ACTIVE, Flag)
        """Is the system's Linux core active?"""

        self.camera_lens_type: BleStatus[Params.MaxLensMode] = BleStatus(
            communicator, StatusId.CAMERA_LENS_TYPE, Params.MaxLensMode
        )
        """Camera lens type (reflects changes to setting 162)."""

        self.video_hindsight: BleStatus[bool] = BleStatus(communicator, StatusId.VIDEO_HINDSIGHT, Flag)
        """Is Video Hindsight Capture Active?"""

        self.scheduled_preset: BleStatus[int] = BleStatus(communicator, StatusId.SCHEDULED_PRESET, Int32ub)
        """Scheduled Capture Preset ID."""

        self.scheduled_capture: BleStatus[bool] = BleStatus(communicator, StatusId.SCHEDULED_CAPTURE, Flag)
        """Is Scheduled Capture set?"""

        self.creating_preset: BleStatus[bool] = BleStatus(communicator, StatusId.CREATING_PRESET, Flag)
        """Is the camera in the process of creating a custom preset?"""

        self.media_mod_stat: BleStatus[Params.MediaModStatus] = BleStatus(
            communicator, StatusId.MEDIA_MOD_STAT, Params.MediaModStatus
        )
        """Media Mode Status (bitmasked)."""

        self.turbo_mode: BleStatus[bool] = BleStatus(communicator, StatusId.TURBO_MODE, Flag)
        """Is Turbo Transfer active?"""

        self.sd_rating_check_error: BleStatus[bool] = BleStatus(communicator, StatusId.SD_RATING_CHECK_ERROR, Flag)
        """Does sdcard meet specified minimum write speed?"""

        self.sd_write_speed_error: BleStatus[int] = BleStatus(communicator, StatusId.SD_WRITE_SPEED_ERROR, Int8ub)
        """Number of sdcard write speed errors since device booted"""

        self.camera_control: BleStatus[Params.CameraControl] = BleStatus(
            communicator, StatusId.CAMERA_CONTROL, Params.CameraControl
        )
        """Camera control status ID"""

        self.usb_connected: BleStatus[bool] = BleStatus(communicator, StatusId.USB_CONNECTED, Flag)
        """Is the camera connected to a PC via USB?"""

        self.control_allowed_over_usb: BleStatus[bool] = BleStatus(communicator, StatusId.CONTROL_OVER_USB, Flag)
        """Is control allowed over USB?"""

        self.total_sd_space_kb: BleStatus[int] = BleStatus(communicator, StatusId.TOTAL_SD_SPACE_KB, Int32ub)
        """Total space taken up on the SD card in kilobytes"""

        super().__init__(communicator)
