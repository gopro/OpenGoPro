# ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""BLE API for Open GoPro"""

from __future__ import annotations
import logging
import datetime
from typing import Optional, Final

from construct import (
    Int8ub,
    Int32ub,
    Int64ub,
    Flag,
    GreedyBytes,
    GreedyString,
    Struct,
    Padding,
    PaddedString,
    this,
    Hex,
    Int16ub,
    Int16sb,
)

from open_gopro import proto
from open_gopro.responses import GoProResp, CustomBytesParser, BytesBuilder
from open_gopro.interface import GoProBle, Commands, BleCommand
from open_gopro.api.builders import (
    build_enum_adapter,
    DeprecatedAdapter,
    protobuf_construct_adapter_factory,
    BleStatus,
    BleSetting,
    BleAsyncResponse,
    BleWriteCommand,
    RegisterUnregisterAll,
    BleReadCommand,
    BleProtoCommand,
)
from open_gopro.constants import ActionId, FeatureId, CmdId, QueryCmdId, SettingId, StatusId, GoProUUIDs
from . import params as Params

logger = logging.getLogger(__name__)


class BleCommands(Commands[BleCommand, CmdId]):
    """All of the BLE commands.

    To be used as a delegate for a GoProBle instance to build commands

    All of these return a GoProResp
    """

    # pylint: disable = missing-class-docstring, arguments-differ, useless-super-delegation
    def __init__(self, communicator: GoProBle):
        """Constructor

        Args:
            communicator (GoProBle): GoPro BLE communicator that will send the commands
        """
        ######################################################################################################
        #                          BLE WRITE COMMANDS
        ######################################################################################################

        class SetShutter(BleWriteCommand):
            def __call__(self, shutter: Params.Toggle) -> GoProResp:
                """Set the Shutter

                Args:
                    shutter (open_gopro.api.params.Toggle): on or off

                Returns:
                    GoProResp: status of command
                """
                return super().__call__(shutter=shutter)

        #: Sphinx docstring redirect
        self.set_shutter = SetShutter(communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_SHUTTER, Int8ub)

        class TagHilight(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Tag a highlight during encoding

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.tag_hilight = TagHilight(communicator, GoProUUIDs.CQ_COMMAND, CmdId.TAG_HILIGHT)

        class PowerDown(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Power Down the camera

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.power_down = PowerDown(communicator, GoProUUIDs.CQ_COMMAND, CmdId.POWER_DOWN)

        class Sleep(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Put the camera in standby

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.sleep = Sleep(communicator, GoProUUIDs.CQ_COMMAND, CmdId.SLEEP)

        class EnableWifi(BleWriteCommand):
            def __call__(self, enable: bool) -> GoProResp:
                """Enable / disable the Wi-Fi Access Point.

                Args:
                    enable (bool): True to enable, False to disable

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__(enable=enable)

        #: Sphinx docstring redirect
        self.enable_wifi_ap = EnableWifi(communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_WIFI, Int8ub)

        class GetHardwareInfo(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get the model number, board, type, firmware version, serial number, and AP info

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_hardware_info = GetHardwareInfo(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_HW_INFO,
            parser=Struct(
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
                "ap_mac" / PaddedString(this.ap_mac_len, "utf-8"),
            ),
        )

        class LoadPresetGroup(BleWriteCommand):
            def __call__(self, group: Params.PresetGroup) -> GoProResp:
                """Load a Preset Group.

                Once complete, the most recently used preset in this group will be active.


                Args:
                    group (open_gopro.api.params.PresetGroup): preset group to load

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__(group=group)

        #: Sphinx docstring redirect
        self.load_preset_group = LoadPresetGroup(
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET_GROUP, Int16ub
        )

        class LoadPreset(BleWriteCommand):
            def __call__(self, preset: int) -> GoProResp:
                """Load a Preset

                The int ID value can be found from the get_preset_status command

                Args:
                    preset (int): preset ID to load

                Returns:
                    GoProResp: command status
                """
                return super().__call__(preset=preset)

        #: Sphinx docstring redirect
        self.load_preset = LoadPreset(communicator, GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET, Int32ub)

        class SetThirdPartyClientInfo(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Flag as third party app

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.set_third_party_client_info = SetThirdPartyClientInfo(
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_THIRD_PARTY_CLIENT_INFO
        )

        class GetOgpApiVersion(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get Open GoPro API Version

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_open_gopro_api_version = GetOgpApiVersion(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_THIRD_PARTY_API_VERSION,
            parser=Struct(Padding(1), "major" / Int8ub, Padding(1), "minor" / Int8ub),
        )

        class GetCameraStatuses(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get all of the camera's statuses

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_camera_statuses = GetCameraStatuses(
            communicator, GoProUUIDs.CQ_QUERY, CmdId.GET_CAMERA_STATUSES
        )

        class GetCameraSettings(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get all of the camera's settings

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_camera_settings = GetCameraSettings(
            communicator, GoProUUIDs.CQ_QUERY, CmdId.GET_CAMERA_SETTINGS
        )

        class GetCameraCapabilities(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get the current capabilities of each camera setting

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_camera_capabilities = GetCameraCapabilities(
            communicator, GoProUUIDs.CQ_QUERY, CmdId.GET_CAMERA_CAPABILITIES
        )

        class SetDateTime(BleWriteCommand):
            def __call__(self, date_time: datetime.datetime) -> GoProResp:
                """Set the camera's date and time (non timezone / DST version)

                Args:
                    date_time (datetime.datetime): Date and time to set (Timezone will be ignored)

                Returns:
                    GoProResp: command status
                """
                return super().__call__(date_time=date_time)

        #: Sphinx docstring redirect
        self.set_date_time = SetDateTime(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.SET_DATE_TIME,
            param_builder=BleParserBuilders.DateTime(),
        )

        class GetDateTime(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get the camera's date and time (non timezone / DST version)

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_date_time = GetDateTime(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_DATE_TIME,
            parser=BleParserBuilders.DateTime(),
        )

        class SetDateTimeTzDst(BleWriteCommand):
            def __call__(self, date_time: datetime.datetime, tz_offset: int, is_dst: bool) -> GoProResp:
                """Set the camera's date and time with timezone and DST

                Args:
                    date_time (datetime.datetime): date and time
                    tz_offset (int): timezone as UTC offset
                    is_dst (bool): is daylight savings time?

                Returns:
                    GoProResp: command status
                """
                return super().__call__(date_time=date_time, tz_offset=tz_offset, is_dst=is_dst)

        #: Sphinx docstring redirect
        self.set_date_time_tz_dst = SetDateTimeTzDst(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.SET_DATE_TIME_DST,
            param_builder=BleParserBuilders.DateTime(),
        )

        class GetDateTimeTzDst(BleWriteCommand):
            def __call__(self) -> GoProResp:
                """Get the camera's date and time with timezone / DST

                Returns:
                    GoProResp: response as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_date_time_tz_dst = GetDateTimeTzDst(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_DATE_TIME_DST,
            parser=BleParserBuilders.DateTime(),
        )

        ######################################################################################################
        #                          BLE DIRECT CHARACTERISTIC READ COMMANDS
        ######################################################################################################

        #: Sphinx docstring redirect
        self.get_wifi_ssid = BleReadCommand(
            communicator, GoProUUIDs.WAP_SSID, Struct("ssid" / GreedyString("utf-8"))
        )
        """Get the Wifi SSID.

        Returns:
            GoProResp: command status and SSID
        """

        #: Sphinx docstring redirect
        self.get_wifi_password = BleReadCommand(
            communicator, GoProUUIDs.WAP_PASSWORD, Struct("password" / GreedyString("utf-8"))
        )
        """Get the Wifi password.

        Returns:
            GoProResp: command status and password
        """

        ######################################################################################################
        #                          REGISTER / UNREGISTER ALL COMMANDS
        ######################################################################################################

        self.register_for_all_statuses = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.REGISTER_ALL_STATUSES,
            producer=(StatusId, QueryCmdId.STATUS_VAL_PUSH),
            action=RegisterUnregisterAll.Action.REGISTER,
        )
        """Register push notifications for all statuses

        Returns:
            GoProResp: command status and current value of all statuses
        """

        self.unregister_for_all_statuses = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.UNREGISTER_ALL_STATUSES,
            producer=(StatusId, QueryCmdId.STATUS_VAL_PUSH),
            action=RegisterUnregisterAll.Action.UNREGISTER,
        )
        """Unregister push notifications for all statuses

        Returns:
            GoProResp: command status
        """

        self.register_for_all_settings = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.REGISTER_ALL_SETTINGS,
            producer=(SettingId, QueryCmdId.SETTING_VAL_PUSH),
            action=RegisterUnregisterAll.Action.REGISTER,
        )
        """Register push notifications for all settings

        Returns:
            GoProResp: command status and current value of all settings
        """

        self.unregister_for_all_settings = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.UNREGISTER_ALL_SETTINGS,
            producer=(SettingId, QueryCmdId.SETTING_VAL_PUSH),
            action=RegisterUnregisterAll.Action.UNREGISTER,
        )
        """Unregister push notifications for all settings

        Returns:
            GoProResp: command status
        """

        self.register_for_all_capabilities = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.REGISTER_ALL_CAPABILITIES,
            producer=(SettingId, QueryCmdId.SETTING_CAPABILITY_PUSH),
            action=RegisterUnregisterAll.Action.REGISTER,
        )
        """Register push notifications for all capabilities

        Returns:
            GoProResp: command status and current value of all capabilities
        """

        self.unregister_for_all_capabilities = RegisterUnregisterAll(
            communicator,
            GoProUUIDs.CQ_QUERY,
            CmdId.UNREGISTER_ALL_CAPABILITIES,
            producer=(SettingId, QueryCmdId.SETTING_CAPABILITY_PUSH),
            action=RegisterUnregisterAll.Action.UNREGISTER,
        )
        """Unregister push notifications for all capabilities

        Returns:
            GoProResp: command status
        """

        ######################################################################################################
        #                          PROTOBUF COMMANDS
        ######################################################################################################

        class SetCameraControl(BleProtoCommand):
            def __call__(self, control: Params.CameraControlStatus) -> GoProResp:
                """Tell the camera that the app (i.e. External Control) wishes to claim control of the camera.

                Args:
                    control (bool): True to enable, False to disable.

                Returns:
                    GoProResp: command status of request
                """
                return super().__call__(camera_control_status=control)

        #: Sphinx docstring redirect
        self.set_camera_control = SetCameraControl(
            communicator,
            uuid=GoProUUIDs.CQ_COMMAND,
            feature_id=FeatureId.COMMAND,
            action_id=ActionId.SET_CAMERA_CONTROL,
            response_action_id=ActionId.SET_CAMERA_CONTROL_RSP,
            request_proto=proto.RequestSetCameraControlStatus,
            response_proto=proto.ResponseGeneric,
        )

        class TurboMode(BleProtoCommand):
            def __call__(self, active: bool) -> GoProResp:
                """Enable / disable turbo mode.

                Args:
                    active (bool): True to enable, False to disable.

                Returns:
                    GoProResp: command status of request
                """
                return super().__call__(active=active)

        #: Sphinx docstring redirect
        self.set_turbo_mode = TurboMode(
            communicator,
            uuid=GoProUUIDs.CQ_COMMAND,
            feature_id=FeatureId.COMMAND,
            action_id=ActionId.SET_TURBO_MODE,
            response_action_id=ActionId.SET_TURBO_MODE_RSP,
            request_proto=proto.RequestSetTurboActive,
            response_proto=proto.ResponseGeneric,
        )

        class GetPresetStatus(BleProtoCommand):
            def __call__(
                self,
                register_preset_status: Optional[list[Params.RegisterPreset]] = None,
                unregister_preset_status: Optional[list[Params.RegisterPreset]] = None,
            ) -> GoProResp:
                """Get information about what Preset Groups and Presets the camera supports in its current state

                Also optionally (un)register for preset / group preset modified notifications which  will be
                sent asynchronously as :py:attr:`open_gopro.constants.ActionId.PRESET_MODIFIED_NOTIFICATION`

                Args:
                    register_preset_status (list[open_gopro.api.params.RegisterPreset], Optional): Types of
                        preset modified updates to register for. Defaults to None.
                    unregister_preset_status (list[open_gopro.api.params.RegisterPreset], Optional): Types of
                        preset modified updates to unregister for. Defaults to None.

                Returns:
                    GoProResp: JSON data describing all currently available presets
                """
                return super().__call__(
                    register_preset_status=register_preset_status or [],
                    unregister_preset_status=unregister_preset_status or [],
                )

        #: Sphinx docstring redirect
        self.get_preset_status = GetPresetStatus(
            communicator,
            uuid=GoProUUIDs.CQ_QUERY,
            feature_id=FeatureId.QUERY,
            action_id=ActionId.GET_PRESET_STATUS,
            response_action_id=ActionId.GET_PRESET_STATUS_RSP,
            request_proto=proto.RequestGetPresetStatus,
            response_proto=proto.NotifyPresetStatus,
            additional_matching_ids={ActionId.PRESET_MODIFIED_NOTIFICATION},
        )

        class RequestWifiConnect(BleProtoCommand):
            def __call__(self, ssid: str, password: str) -> GoProResp:
                """Request the camera to connect to a WiFi network.

                Updates will be sent as :py:attr:`open_gopro.constants.ActionId.NOTIF_PROVIS_STATE`

                Args:
                    ssid (str): SSID to connect to
                    password (str): password of WiFi network

                Returns:
                    GoProResp: Command status of request
                """
                return super().__call__(ssid=ssid, password=password)

        #: Sphinx docstring redirect
        self.request_wifi_connect = RequestWifiConnect(
            communicator,
            uuid=GoProUUIDs.CM_NET_MGMT_COMM,
            feature_id=FeatureId.NETWORK_MANAGEMENT,
            action_id=ActionId.REQUEST_WIFI_CONNECT,
            response_action_id=ActionId.REQUEST_WIFI_CONNECT_RSP,
            request_proto=proto.RequestConnectNew,
            response_proto=proto.ResponseConnectNew,
            additional_matching_ids={ActionId.REQUEST_WIFI_CONNECT_RSP},
        )

        class SetLivestreamMode(BleProtoCommand):
            def __call__(
                self,
                url: str,
                window_size: Params.WindowSize,
                cert: bytes,
                minimum_bitrate: int,
                maximum_bitrate: int,
                starting_bitrate: int,
                lens: Params.LensType,
            ) -> GoProResp:
                """Initiate livestream to any site that accepts an RTMP URL and simultaneously encode to camera.

                Args:
                    url (str): url used to stream. Set to empty string to invalidate/cancel stream
                    window_size (open_gopro.api.params.WindowSize): Streaming video resolution
                    cert (bytes): Certificate from a trusted root for streaming services that use encryption
                    minimum_bitrate (int): Desired minimum streaming bitrate (>= 800)
                    maximum_bitrate (int): Desired maximum streaming bitrate (<= 8000)
                    starting_bitrate (int): Initial streaming bitrate (honored if 800 <= value <= 8000)
                    lens (open_gopro.api.params.LensType): Streaming Field of View

                Returns:
                    GoProResp: command status of request
                """
                return super().__call__(
                    url=url,
                    encode=True,
                    window_size=window_size,
                    cert=cert,
                    minimum_bitrate=minimum_bitrate,
                    maximum_bitrate=maximum_bitrate,
                    starting_bitrate=starting_bitrate,
                    lens=lens,
                )

        #: Sphinx docstring redirect
        self.set_livestream_mode = SetLivestreamMode(
            communicator,
            uuid=GoProUUIDs.CQ_COMMAND,
            feature_id=FeatureId.COMMAND,
            action_id=ActionId.SET_LIVESTREAM_MODE,
            response_action_id=ActionId.SET_LIVESTREAM_MODE_RSP,
            request_proto=proto.RequestSetLiveStreamMode,
            response_proto=proto.ResponseGeneric,
        )

        class LivestreamStatus(BleProtoCommand):
            def __call__(
                self,
                register: Optional[list[Params.RegisterLiveStream]] = None,
                unregister: Optional[list[Params.RegisterLiveStream]] = None,
            ) -> GoProResp:
                return super().__call__(
                    register_live_stream_status=register or [], unregister_live_stream_status=unregister or []
                )

        self.register_livestream_status = LivestreamStatus(
            communicator,
            uuid=GoProUUIDs.CQ_QUERY,
            feature_id=FeatureId.QUERY,
            action_id=ActionId.GET_LIVESTREAM_STATUS,
            response_action_id=ActionId.LIVESTREAM_STATUS_RSP,
            request_proto=proto.RequestGetLiveStreamStatus,
            response_proto=proto.NotifyLiveStreamStatus,
            additional_matching_ids={ActionId.LIVESTREAM_STATUS_NOTIF},
        )

        super().__init__(communicator)


class BleSettings(Commands[BleSetting, SettingId]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all BLE Settings.

    To be used by a GoProBle delegate to build setting commands.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (type[Params]): the set of parameters to use to build the settings
    """

    def __init__(self, communicator: GoProBle):

        self.resolution = BleSetting[Params.Resolution](
            communicator, SettingId.RESOLUTION, build_enum_adapter(Params.Resolution)
        )
        """Resolution. Set with :py:class:`open_gopro.api.params.Resolution`"""

        self.fps = BleSetting[Params.FPS](communicator, SettingId.FPS, build_enum_adapter(Params.FPS))
        """Frames per second. Set with :py:class:`open_gopro.api.params.FPS`"""

        self.auto_off = BleSetting[Params.AutoOff](
            communicator, SettingId.AUTO_OFF, build_enum_adapter(Params.AutoOff)
        )
        """Set the auto off time. Set with :py:class:`open_gopro.api.params.AutoOff`"""

        self.video_field_of_view = BleSetting[Params.VideoFOV](
            communicator, SettingId.VIDEO_FOV, build_enum_adapter(Params.VideoFOV)
        )
        """Video FOV. Set with :py:class:`open_gopro.api.params.VideoFOV`"""

        self.photo_field_of_view = BleSetting[Params.PhotoFOV](
            communicator, SettingId.PHOTO_FOV, build_enum_adapter(Params.PhotoFOV)
        )
        """Photo FOV. Set with :py:class:`open_gopro.api.params.PhotoFOV`"""

        self.multi_shot_field_of_view = BleSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV, build_enum_adapter(Params.MultishotFOV)
        )
        """Multi-shot FOV. Set with :py:class:`open_gopro.api.params.MultishotFOV`"""

        self.led = BleSetting[Params.LED](communicator, SettingId.LED, build_enum_adapter(Params.LED))
        """Set the LED options (or also send the BLE keep alive signal). Set with :py:class:`open_gopro.api.params.LED`"""

        self.max_lens_mode = BleSetting[Params.MaxLensMode](
            communicator, SettingId.MAX_LENS_MOD, build_enum_adapter(Params.MaxLensMode)
        )
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.api.params.MaxLensMode`"""

        self.hypersmooth = BleSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH, build_enum_adapter(Params.HypersmoothMode)
        )
        """Set / disable hypersmooth. Set with :py:class:`open_gopro.api.params.HypersmoothMode`"""

        self.video_performance_mode = BleSetting[Params.PerformanceMode](
            communicator,
            SettingId.VIDEO_PERFORMANCE_MODE,
            build_enum_adapter(Params.PerformanceMode),
        )
        """Video Performance Mode. Set with :py:class:`open_gopro.api.params.PerformanceMode`"""

        self.media_format = BleSetting[Params.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT, build_enum_adapter(Params.MediaFormat)
        )
        """Set the media format. Set with :py:class:`open_gopro.api.params.MediaFormat`"""

        self.anti_flicker = BleSetting[Params.AntiFlicker](
            communicator,
            SettingId.ANTI_FLICKER,
            build_enum_adapter(Params.AntiFlicker),
        )
        """Anti Flicker frequency. Set with :py:class:`open_gopro.api.params.AntiFlicker`"""

        self.camera_ux_mode = BleSetting[Params.CameraUxMode](
            communicator,
            SettingId.CAMERA_UX_MODE,
            build_enum_adapter(Params.CameraUxMode),
        )
        """Camera controls configuration. Set with :py:class:`open_gopro.api.params.CameraUxMode`"""

        self.video_easy_mode = BleSetting[Params.Speed](
            communicator,
            SettingId.VIDEO_EASY_MODE,
            build_enum_adapter(Params.Speed),
        )
        """Video easy mode speed. Set with :py:class:`open_gopro.api.params.Speed`"""

        self.photo_easy_mode = BleSetting[Params.PhotoEasyMode](
            communicator,
            SettingId.PHOTO_EASY_MODE,
            build_enum_adapter(Params.PhotoEasyMode),
        )
        """Night Photo easy mode. Set with :py:class:`open_gopro.api.params.PhotoEasyMode`"""

        self.wifi_band = BleSetting[Params.WifiBand](
            communicator,
            SettingId.WIFI_BAND,
            build_enum_adapter(Params.WifiBand),
        )
        """Current WiFi band being used. Set with :py:class:`open_gopro.api.params.WifiBand`"""

        self.star_trail_length = BleSetting[Params.StarTrailLength](
            communicator,
            SettingId.STAR_TRAIL_LENGTH,
            build_enum_adapter(Params.StarTrailLength),
        )
        """Multi shot star trail length. Set with :py:class:`open_gopro.api.params.StarTrailLength`"""

        self.system_video_mode = BleSetting[Params.SystemVideoMode](
            communicator,
            SettingId.SYSTEM_VIDEO_MODE,
            build_enum_adapter(Params.SystemVideoMode),
        )
        """System video mode. Set with :py:class:`open_gopro.api.params.SystemVideoMode`"""

        self.video_horizon_leveling = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.VIDEO_HORIZON_LEVELING,
            build_enum_adapter(Params.HorizonLeveling),
        )
        """Lock / unlock horizon leveling for video. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        self.photo_horizon_leveling = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.PHOTO_HORIZON_LEVELING,
            build_enum_adapter(Params.HorizonLeveling),
        )
        """Lock / unlock horizon leveling for photo. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        super().__init__(communicator)


class BleAsyncResponses:
    """These are responses whose ID's are not associated with any commands"""

    generic_response: Final = Struct("unparsed" / GreedyBytes)

    responses = [
        BleAsyncResponse(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.NOTIF_PROVIS_STATE,
            protobuf_construct_adapter_factory(proto.NotifProvisioningState),
        ),
        BleAsyncResponse(FeatureId.QUERY, ActionId.INTERNAL_FF, generic_response),
    ]

    @classmethod
    def add_parsers(cls) -> None:
        """Add all of the defined asynchronous responses to the global parser map"""
        for response in cls.responses:
            GoProResp._add_global_parser(response.action_id, response.parser)
            GoProResp._add_feature_action_id_mapping(response.feature_id, response.action_id)


class BleStatuses(Commands[BleStatus, StatusId]):
    """All of the BLE Statuses.

    To be used by a GoProBle delegate to build status commands.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (type[Params]): the set of parameters to use to build the statuses
    """

    def __init__(self, communicator: GoProBle) -> None:
        self.batt_present: BleStatus = BleStatus(communicator, StatusId.BATT_PRESENT, Flag)
        """Is the system's internal battery present?"""

        self.batt_level: BleStatus = BleStatus(communicator, StatusId.BATT_LEVEL, Int8ub)
        """Rough approximation of internal battery level in bars."""

        self.ext_batt_present: BleStatus = BleStatus(communicator, StatusId.EXT_BATT_PRESENT, Flag)
        """Is an external battery connected?"""

        self.ext_batt_level: BleStatus = BleStatus(communicator, StatusId.EXT_BATT_LEVEL, Int8ub)
        """External battery power level in percent."""

        self.system_hot: BleStatus = BleStatus(communicator, StatusId.SYSTEM_HOT, Flag)
        """Is the system currently overheating?"""

        self.system_busy: BleStatus = BleStatus(communicator, StatusId.SYSTEM_BUSY, Flag)
        """Is the camera busy?"""

        self.quick_capture: BleStatus = BleStatus(communicator, StatusId.QUICK_CAPTURE, Flag)
        """Is quick capture feature enabled?"""

        self.encoding_active: BleStatus = BleStatus(communicator, StatusId.ENCODING, Flag)
        """Is the camera currently encoding (i.e. capturing photo / video)?"""

        self.lcd_lock_active: BleStatus = BleStatus(communicator, StatusId.LCD_LOCK_ACTIVE, Flag)
        """Is the LCD lock currently active?"""

        self.video_progress: BleStatus = BleStatus(communicator, StatusId.VIDEO_PROGRESS, Int32ub)
        """When encoding video, this is the duration (seconds) of the video so far; 0 otherwise."""

        self.wireless_enabled: BleStatus = BleStatus(communicator, StatusId.WIRELESS_ENABLED, Flag)
        """Are Wireless Connections enabled?"""

        self.pair_state: BleStatus = BleStatus(
            communicator, StatusId.PAIR_STATE, build_enum_adapter(Params.PairState)
        )
        """What is the pair state?"""

        self.pair_type: BleStatus = BleStatus(
            communicator, StatusId.PAIR_TYPE, build_enum_adapter(Params.PairType)
        )
        """The last type of pairing that the camera was engaged in."""

        self.pair_time: BleStatus = BleStatus(communicator, StatusId.PAIR_TIME, Int32ub)
        """	Time (milliseconds) since boot of last successful pairing complete action."""

        self.wap_scan_state: BleStatus = BleStatus(
            communicator, StatusId.WAP_SCAN_STATE, build_enum_adapter(Params.WAPState)
        )
        """State of current scan for Wifi Access Points. Appears to only change for CAH-related scans."""

        self.wap_scan_time: BleStatus = BleStatus(communicator, StatusId.WAP_SCAN_TIME, Int8ub)
        """The time, in milliseconds since boot that the Wifi Access Point scan completed."""

        self.wap_prov_stat: BleStatus = BleStatus(
            communicator, StatusId.WAP_PROV_STAT, build_enum_adapter(Params.WAPState)
        )
        """Wifi AP provisioning state."""

        self.remote_ctrl_ver: BleStatus = BleStatus(communicator, StatusId.REMOTE_CTRL_VER, Int8ub)
        """What is the remote control version?"""

        self.remote_ctrl_conn: BleStatus = BleStatus(communicator, StatusId.REMOTE_CTRL_CONN, Flag)
        """Is the remote control connected?"""

        self.pair_state2: BleStatus = BleStatus(communicator, StatusId.PAIR_STATE2, Int8ub)
        """Wireless Pairing State."""

        self.wlan_ssid: BleStatus = BleStatus(communicator, StatusId.WLAN_SSID, GreedyString(encoding="utf-8"))
        """Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.ap_ssid: BleStatus = BleStatus(communicator, StatusId.AP_SSID, GreedyString(encoding="utf-8"))
        """Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.app_count: BleStatus = BleStatus(communicator, StatusId.APP_COUNT, Int8ub)
        """The number of wireless devices connected to the camera."""

        self.preview_enabled: BleStatus = BleStatus(communicator, StatusId.PREVIEW_ENABLED, Flag)
        """Is preview stream enabled?"""

        self.sd_status: BleStatus = BleStatus(
            communicator, StatusId.SD_STATUS, build_enum_adapter(Params.SDStatus)
        )
        """Primary Storage Status."""

        self.photos_rem: BleStatus = BleStatus(communicator, StatusId.PHOTOS_REM, Int32ub)
        """How many photos can be taken before sdcard is full?"""

        self.video_rem: BleStatus = BleStatus(communicator, StatusId.VIDEO_REM, Int32ub)
        """How many minutes of video can be captured with current settings before sdcard is full?"""

        self.num_group_photo: BleStatus = BleStatus(communicator, StatusId.NUM_GROUP_PHOTO, Int32ub)
        """How many group photos can be taken with current settings before sdcard is full?"""

        self.num_group_video: BleStatus = BleStatus(communicator, StatusId.NUM_GROUP_VIDEO, Int32ub)
        """Total number of group videos on sdcard."""

        self.num_total_photo: BleStatus = BleStatus(communicator, StatusId.NUM_TOTAL_PHOTO, Int32ub)
        """Total number of photos on sdcard."""

        self.num_total_video: BleStatus = BleStatus(communicator, StatusId.NUM_TOTAL_VIDEO, Int32ub)
        """Total number of videos on sdcard."""

        self.deprecated_40: BleStatus = BleStatus(
            communicator, StatusId.DEPRECATED_40, DeprecatedAdapter(GreedyString(encoding="utf-8"))
        )
        """This status is deprecated."""

        self.ota_stat: BleStatus = BleStatus(
            communicator, StatusId.OTA_STAT, build_enum_adapter(Params.OTAStatus)
        )
        """The current status of Over The Air (OTA) update."""

        self.download_cancel_pend: BleStatus = BleStatus(communicator, StatusId.DOWNLOAD_CANCEL_PEND, Flag)
        """Is download firmware update cancel request pending?"""

        self.mode_group: BleStatus = BleStatus(communicator, StatusId.MODE_GROUP, Int8ub)
        """Current mode group (deprecated in HERO8)."""

        self.locate_active: BleStatus = BleStatus(communicator, StatusId.LOCATE_ACTIVE, Flag)
        """Is locate camera feature active?"""

        self.multi_count_down: BleStatus = BleStatus(communicator, StatusId.MULTI_COUNT_DOWN, Int32ub)
        """The current timelapse interval countdown value (e.g. 5...4...3...2...1...)."""

        self.space_rem: BleStatus = BleStatus(communicator, StatusId.SPACE_REM, Int64ub)
        """Remaining space on the sdcard in Kilobytes."""

        self.streaming_supp: BleStatus = BleStatus(communicator, StatusId.STREAMING_SUPP, Flag)
        """Is streaming supports in current recording/flatmode/secondary-stream?"""

        self.wifi_bars: BleStatus = BleStatus(communicator, StatusId.WIFI_BARS, Int8ub)
        """Wifi signal strength in bars."""

        self.current_time_ms: BleStatus = BleStatus(communicator, StatusId.CURRENT_TIME_MS, Int32ub)
        """System time in milliseconds since system was booted."""

        self.num_hilights: BleStatus = BleStatus(communicator, StatusId.NUM_HILIGHTS, Int8ub)
        """The number of hilights in encoding video (set to 0 when encoding stops)."""

        self.last_hilight: BleStatus = BleStatus(communicator, StatusId.LAST_HILIGHT, Int32ub)
        """Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)."""

        self.next_poll: BleStatus = BleStatus(communicator, StatusId.NEXT_POLL, Int32ub)
        """The min time between camera status updates (msec). Do not poll for status more often than this."""

        self.analytics_rdy: BleStatus = BleStatus(
            communicator, StatusId.ANALYTICS_RDY, build_enum_adapter(Params.AnalyticsState)
        )
        """The current state of camera analytics."""

        self.analytics_size: BleStatus = BleStatus(communicator, StatusId.ANALYTICS_SIZE, Int32ub)
        """The size (units??) of the analytics file."""

        self.in_context_menu: BleStatus = BleStatus(communicator, StatusId.IN_CONTEXT_MENU, Flag)
        """Is the camera currently in a contextual menu (e.g. Preferences)?"""

        self.timelapse_rem: BleStatus = BleStatus(communicator, StatusId.TIMELAPSE_REM, Int32ub)
        """How many min of Timelapse video can be captured with current settings before sdcard is full?"""

        self.exposure_type: BleStatus = BleStatus(
            communicator, StatusId.EXPOSURE_TYPE, build_enum_adapter(Params.ExposureMode)
        )
        """Liveview Exposure Select Mode."""

        self.exposure_x: BleStatus = BleStatus(communicator, StatusId.EXPOSURE_X, Int8ub)
        """Liveview Exposure Select for y-coordinate (percent)."""

        self.exposure_y: BleStatus = BleStatus(communicator, StatusId.EXPOSURE_Y, Int8ub)
        """Liveview Exposure Select for y-coordinate (percent)."""

        self.gps_stat: BleStatus = BleStatus(communicator, StatusId.GPS_STAT, Flag)
        """Does the camera currently have a GPS lock?"""

        self.ap_state: BleStatus = BleStatus(communicator, StatusId.AP_STATE, Flag)
        """Is the Wifi radio enabled?"""

        self.int_batt_per: BleStatus = BleStatus(communicator, StatusId.INT_BATT_PER, Int8ub)
        """Internal battery level (percent)."""

        self.acc_mic_stat: BleStatus = BleStatus(
            communicator, StatusId.ACC_MIC_STAT, build_enum_adapter(Params.ExposureMode)
        )
        """Microphone Accessory status."""

        self.digital_zoom: BleStatus = BleStatus(communicator, StatusId.DIGITAL_ZOOM, Int8ub)
        """	Digital Zoom level (percent)."""

        self.wireless_band: BleStatus = BleStatus(
            communicator, StatusId.WIRELESS_BAND, build_enum_adapter(Params.WifiBand)
        )
        """Wireless Band."""

        self.dig_zoom_active: BleStatus = BleStatus(communicator, StatusId.DIG_ZOOM_ACTIVE, Flag)
        """Is Digital Zoom feature available?"""

        self.mobile_video: BleStatus = BleStatus(communicator, StatusId.MOBILE_VIDEO, Flag)
        """Are current video settings mobile friendly? (related to video compression and frame rate)."""

        self.first_time: BleStatus = BleStatus(communicator, StatusId.FIRST_TIME, Flag)
        """Is the camera currently in First Time Use (FTU) UI flow?"""

        self.sec_sd_stat: BleStatus = BleStatus(
            communicator, StatusId.SEC_SD_STAT, build_enum_adapter(Params.SDStatus)
        )
        """Secondary Storage Status (exclusive to Superbank)."""

        self.band_5ghz_avail: BleStatus = BleStatus(communicator, StatusId.BAND_5GHZ_AVAIL, Flag)
        """Is 5GHz wireless band available?"""

        self.system_ready: BleStatus = BleStatus(communicator, StatusId.SYSTEM_READY, Flag)
        """Is the system ready to accept commands?"""

        self.batt_ok_ota: BleStatus = BleStatus(communicator, StatusId.BATT_OK_OTA, Flag)
        """Is the internal battery charged sufficiently to start Over The Air (OTA) update?"""

        self.video_low_temp: BleStatus = BleStatus(communicator, StatusId.VIDEO_LOW_TEMP, Flag)
        """Is the camera getting too cold to continue recording?"""

        self.orientation: BleStatus = BleStatus(
            communicator, StatusId.ORIENTATION, build_enum_adapter(Params.Orientation)
        )
        """The rotational orientation of the camera."""

        self.thermal_mit_mode: BleStatus = BleStatus(
            communicator, StatusId.DEPRECATED_92, DeprecatedAdapter(Flag)
        )
        """This status is deprecated."""

        self.zoom_encoding: BleStatus = BleStatus(communicator, StatusId.ZOOM_ENCODING, Flag)
        """Is this camera capable of zooming while encoding (static value based on model, not settings)?"""

        self.flatmode_id: BleStatus = BleStatus(
            communicator, StatusId.FLATMODE_ID, build_enum_adapter(Params.Flatmode)
        )
        """Current flatmode ID."""

        self.logs_ready: BleStatus = BleStatus(communicator, StatusId.LOGS_READY, Flag)
        """	Are system logs ready to be downloaded?"""

        self.deprecated_92: BleStatus = BleStatus(
            communicator, StatusId.DEPRECATED_92, DeprecatedAdapter(Flag)
        )
        """This status is deprecated."""

        self.video_presets: BleStatus = BleStatus(communicator, StatusId.VIDEO_PRESETS, Int32ub)
        """Current Video Preset (ID)."""

        self.photo_presets: BleStatus = BleStatus(communicator, StatusId.PHOTO_PRESETS, Int32ub)
        """Current Photo Preset (ID)."""

        self.timelapse_presets: BleStatus = BleStatus(communicator, StatusId.TIMELAPSE_PRESETS, Int32ub)
        """	Current Timelapse Preset (ID)."""

        self.presets_group: BleStatus = BleStatus(communicator, StatusId.PRESETS_GROUP, Int32ub)
        """Current Preset Group (ID)."""

        self.active_preset: BleStatus = BleStatus(communicator, StatusId.ACTIVE_PRESET, Int32ub)
        """Currently Preset (ID)."""

        self.preset_modified: BleStatus = BleStatus(communicator, StatusId.PRESET_MODIFIED, Int32ub)
        """Preset Modified Status, which contains an event ID and a preset (group) ID."""

        self.live_burst_rem: BleStatus = BleStatus(communicator, StatusId.LIVE_BURST_REM, Int32ub)
        """How many Live Bursts can be captured before sdcard is full?"""

        self.live_burst_total: BleStatus = BleStatus(communicator, StatusId.LIVE_BURST_TOTAL, Int32ub)
        """Total number of Live Bursts on sdcard."""

        self.capt_delay_active: BleStatus = BleStatus(communicator, StatusId.CAPT_DELAY_ACTIVE, Flag)
        """Is Capture Delay currently active (i.e. counting down)?"""

        self.media_mod_mic_stat: BleStatus = BleStatus(
            communicator,
            StatusId.MEDIA_MOD_MIC_STAT,
            build_enum_adapter(Params.MediaModMicStatus),
        )
        """Media mod State."""

        self.timewarp_speed_ramp: BleStatus = BleStatus(
            communicator, StatusId.TIMEWARP_SPEED_RAMP, build_enum_adapter(Params.TimeWarpSpeed)
        )
        """Time Warp Speed."""

        self.linux_core_active: BleStatus = BleStatus(communicator, StatusId.LINUX_CORE_ACTIVE, Flag)
        """Is the system's Linux core active?"""

        self.camera_lens_type: BleStatus = BleStatus(
            communicator, StatusId.CAMERA_LENS_TYPE, build_enum_adapter(Params.MaxLensMode)
        )
        """Camera lens type (reflects changes to setting 162)."""

        self.video_hindsight: BleStatus = BleStatus(communicator, StatusId.VIDEO_HINDSIGHT, Flag)
        """Is Video Hindsight Capture Active?"""

        self.scheduled_preset: BleStatus = BleStatus(communicator, StatusId.SCHEDULED_PRESET, Int32ub)
        """Scheduled Capture Preset ID."""

        self.scheduled_capture: BleStatus = BleStatus(communicator, StatusId.SCHEDULED_CAPTURE, Flag)
        """Is Scheduled Capture set?"""

        self.creating_preset: BleStatus = BleStatus(communicator, StatusId.CREATING_PRESET, Flag)
        """Is the camera in the process of creating a custom preset?"""

        self.media_mod_stat: BleStatus = BleStatus(
            communicator, StatusId.MEDIA_MOD_STAT, build_enum_adapter(Params.MediaModStatus)
        )
        """Media Mode Status (bitmasked)."""

        self.turbo_mode: BleStatus = BleStatus(communicator, StatusId.TURBO_MODE, Flag)
        """Is Turbo Transfer active?"""

        self.sd_rating_check_error: BleStatus = BleStatus(communicator, StatusId.SD_RATING_CHECK_ERROR, Flag)
        """Does sdcard meet specified minimum write speed?"""

        self.sd_write_speed_error: BleStatus = BleStatus(communicator, StatusId.SD_WRITE_SPEED_ERROR, Int8ub)
        """Number of sdcard write speed errors since device booted"""

        self.camera_control: BleStatus = BleStatus(
            communicator,
            StatusId.CAMERA_CONTROL,
            build_enum_adapter(Params.CameraControlStatus),
        )
        """Camera control status ID"""

        self.usb_connected: BleStatus = BleStatus(communicator, StatusId.USB_CONNECTED, Flag)
        """Is the camera connected to a PC via USB?"""

        self.control_allowed_over_usb: BleStatus = BleStatus(communicator, StatusId.CONTROL_OVER_USB, Flag)
        """Is control allowed over USB?"""

        self.total_sd_space_kb: BleStatus = BleStatus(communicator, StatusId.TOTAL_SD_SPACE_KB, Int8ub)
        """Total space taken up on the SD card in kilobytes"""

        super().__init__(communicator)


# pylint: disable = arguments-renamed
class BleParserBuilders:
    """The collection of custom (i.e. not-construct) parsers and / or builders"""

    class DateTime(CustomBytesParser, BytesBuilder):
        """Handle local and non-local datetime parsing / building"""

        def build(
            self, dt: datetime.datetime, tzone: Optional[int] = None, is_dst: Optional[bool] = None
        ) -> bytes:
            """Build bytestream from datetime and optional local arguments

            Args:
                dt (datetime.datetime): date and time
                tzone (Optional[int], optional): timezone (as UTC offset). Defaults to None.
                is_dst (Optional[bool], optional): is daylight savings time?. Defaults to None.

            Returns:
                bytes: _description_
            """
            byte_data = [*Int16ub.build(dt.year), dt.month, dt.day, dt.hour, dt.minute, dt.second]
            if tzone and is_dst:
                byte_data.extend([*Int16sb.build(tzone), *Flag.build(is_dst)])
            return bytes(byte_data)

        def parse(self, data: bytes) -> dict:
            """Parse bytestream into dict of datetime and potential timezone / dst

            Args:
                data (bytes): bytestream to parse

            Returns:
                dict: dict containing datetime
            """
            is_dst_tz = len(data) == 9
            buf = data[1:]
            year = Int16ub.parse(buf[0:2])

            dt = datetime.datetime(year, *[int(x) for x in buf[2:7]])  # type: ignore
            return (
                dict(datetime=dt)
                if is_dst_tz
                else dict(datetime=dt, tzone=Int16sb.parse(buf[7:9]), dst=bool(buf[9]))
            )
