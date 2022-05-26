# ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""BLE API for Open GoPro"""

from __future__ import annotations
import logging
from datetime import datetime
from typing import List, Optional

from construct import Int8ub, Int32ub, Int64ub, Flag, GreedyString, Struct, Padding, PaddedString, this, Hex

from open_gopro import proto
from open_gopro.responses import GoProResp
from open_gopro.communication_client import GoProBle
from open_gopro.api.builders import (
    BleStatus,
    BleSetting,
    BleWriteNoParamsCommand,
    BleWriteWithParamsCommand,
    RegisterUnregisterAll,
    BleReadCommand,
    BleProtoCommand,
    build_enum_adapter,
    DeprecatedAdapter,
    DateTimeAdapter,
)
from open_gopro.constants import (
    ActionId,
    FeatureId,
    CmdId,
    QueryCmdId,
    SettingId,
    StatusId,
    GoProUUIDs,
)
from . import params as Params

logger = logging.getLogger(__name__)


class BleCommands:
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
        self.set_shutter = BleWriteWithParamsCommand[Params.Shutter](
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_SHUTTER, Int8ub
        )
        """Set shutter on or off.

        Args:
            value (Params.Shutter): on or off

        Returns:
            GoProResp: command status
        """

        self.tag_hilight = BleWriteNoParamsCommand(communicator, GoProUUIDs.CQ_COMMAND, CmdId.TAG_HILIGHT)
        """Tag a highlight during encoding"""

        self.power_down = BleWriteNoParamsCommand(communicator, GoProUUIDs.CQ_COMMAND, CmdId.POWER_DOWN)
        """Power down the camera.

        Returns:
            GoProResp: command status
        """

        self.sleep = BleWriteNoParamsCommand(communicator, GoProUUIDs.CQ_COMMAND, CmdId.SLEEP)
        """Put the camera in standby.

        Returns:
            GoProResp: command status
        """

        self.enable_wifi_ap = BleWriteWithParamsCommand[bool](
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_WIFI, Int8ub
        )
        """Enable / disable the Wi-Fi Access Point.

        Args:
            value (bool): True to enable, False to disable

        Returns:
            GoProResp: command status
        """

        self.get_hardware_info = BleWriteNoParamsCommand(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_HW_INFO,
            response_parser=Struct(
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
        """Get hardware information.

        Returns:
            GoProResp: command status and hardware info (model name, etc.)
        """

        self.load_preset_group = BleWriteWithParamsCommand[Params.PresetGroup](
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET_GROUP, Int32ub
        )
        """Load a Preset Group.

        Once complete, the most recently used preset in this group will be active.

        Args:
            value (Params.PresetGroup): preset group to load.

        Returns:
            GoProResp: command status
        """

        self.load_preset = BleWriteWithParamsCommand[Params.Preset](
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.LOAD_PRESET, Int32ub
        )
        """Load a Preset

        Args:
            value (Params.Preset): preset load.

        Returns:
            GoProResp: command status
        """

        self.set_third_party_client_info = BleWriteNoParamsCommand(
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_THIRD_PARTY_CLIENT_INFO
        )
        """Flag as third party app.

        Returns:
            GoProResp: command status
        """

        self.get_open_gopro_api_version = BleWriteNoParamsCommand(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_THIRD_PARTY_API_VERSION,
            response_parser=Struct(Padding(1), "major" / Int8ub, Padding(1), "minor" / Int8ub),
        )
        """Get Open GoPro API version that is supported by the peer camera.

        Returns:
            GoProResp: command status and version (separate into major and minor fields)
        """

        class TurboMode(BleProtoCommand):
            def __call__(self, active: bool) -> GoProResp:
                return super().__call__(active)

        self.set_turbo_mode = TurboMode(
            communicator,
            uuid=GoProUUIDs.CQ_COMMAND,
            feature_id=FeatureId.COMMAND,
            action_id=ActionId.SET_TURBO_MODE,
            request_proto=proto.RequestSetTurboActive,
            response_proto=proto.ResponseGeneric,
        )
        """Enable / disable turbo mode.

        Args:
            active (bool): True to enable, False to disable.

        Returns:
            GoProResp: result status (EnumResultGeneric)
        """

        class GetPresetStatus(BleProtoCommand):
            def __call__(
                self,
                register_preset_status: Optional[List[Params.RegisterPresetStatus]] = None,
                unregister_preset_status: Optional[List[Params.RegisterPresetStatus]] = None,
            ) -> GoProResp:
                return super().__call__(register_preset_status or [], unregister_preset_status or [])

        self.get_preset_status = GetPresetStatus(
            communicator,
            uuid=GoProUUIDs.CQ_QUERY,
            feature_id=FeatureId.QUERY,
            action_id=ActionId.GET_PRESET_STATUS,
            request_proto=proto.RequestGetPresetStatus,
            response_proto=proto.NotifyPresetStatus,
            additional_matching_action_ids={ActionId.PRESET_MODIFIED_NOTIFICATION},
        )
        """Get information about what Preset Groups and Presets the camera supports in its current state.

        Args:
            register_preset_status (List[Params.RegisterPresetStatus], optional): [TODO]. Defaults to None.
            unregister_preset_status (List[Params.RegisterPresetStatus], optional): [TODO]. Defaults to None.

        Returns:
            GoProResp: TODO
        """

        self.get_wifi_ssid = BleReadCommand(
            communicator, GoProUUIDs.WAP_SSID, Struct("ssid" / GreedyString("utf-8"))
        )
        """Get the Wifi SSID.

        Returns:
            GoProResp: command status and SSID
        """

        self.get_wifi_password = BleReadCommand(
            communicator, GoProUUIDs.WAP_PASSWORD, Struct("password" / GreedyString("utf-8"))
        )
        """Get the Wifi password.

        Returns:
            GoProResp: command status and password
        """

        self.get_camera_statuses = BleWriteNoParamsCommand(
            communicator, GoProUUIDs.CQ_QUERY, CmdId.GET_CAMERA_STATUSES
        )
        """Get all camera statuses.

        Returns:
            GoProResp: command status and current value of all statuses
        """

        self.get_camera_settings = BleWriteNoParamsCommand(
            communicator, GoProUUIDs.CQ_QUERY, CmdId.GET_CAMERA_SETTINGS
        )
        """Get all camera settings.

        Returns:
            GoProResp: command status and current value of all settings
        """

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
            producer=(SettingId, QueryCmdId.STATUS_VAL_PUSH),
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
            producer=(SettingId, QueryCmdId.STATUS_VAL_PUSH),
            action=RegisterUnregisterAll.Action.UNREGISTER,
        )
        """Unregister push notifications for all settings

        Returns:
            GoProResp: command status
        """

        # TODO
        # self.register_for_all_capabilities

        self.set_date_time = BleWriteWithParamsCommand[datetime](
            communicator, GoProUUIDs.CQ_COMMAND, CmdId.SET_DATE_TIME, DateTimeAdapter(Int8ub[7])
        )
        """Set the camera's date and time"""

        self.get_date_time = BleWriteNoParamsCommand(
            communicator,
            GoProUUIDs.CQ_COMMAND,
            CmdId.GET_DATE_TIME,
            Struct("date_time" / DateTimeAdapter(Int8ub[8])),
        )
        """Get the camera's date and time"""

        class SetCameraControl(BleProtoCommand):
            def __call__(self, control: Params.CameraControlStatus) -> GoProResp:
                return super().__call__(control)

        self.set_camera_control = SetCameraControl(
            communicator,
            uuid=GoProUUIDs.CQ_COMMAND,
            feature_id=FeatureId.COMMAND,
            action_id=ActionId.SET_CAMERA_CONTROL,
            request_proto=proto.RequestSetCameraControlStatus,
            response_proto=proto.ResponseGeneric,
        )
        """Enable / disable turbo mode.

        Args:
            active (bool): True to enable, False to disable.

        Returns:
            GoProResp: result status (EnumResultGeneric)
        """


class BleSettings:
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all BLE Settings.

    To be used by a GoProBle delegate to build setting commands.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (Type[Params]): the set of parameters to use to build the settings
    """

    class Iterator:
        """Iterator to iterate through a BleSettings instance's attributes

        Does not include the 'communicator' instance.
        """

        def __init__(self, settings: "BleSettings"):
            self._index = 0
            self._setting_attributes = list(settings.__dict__.values())[1:]  # Skip communicator

        def __next__(self) -> BleSetting:
            """Return next attribute

            Raises:
                StopIteration: Iteration has completed

            Returns:
                BleSetting: next attribute
            """
            if self._index < len(self._setting_attributes):
                setting = self._setting_attributes[self._index]
                self._index += 1
                return setting
            # End of Iteration
            raise StopIteration

    def __init__(self, communicator: GoProBle):
        self.communicator = communicator

        self.resolution: BleSetting = BleSetting[Params.Resolution](
            self.communicator, SettingId.RESOLUTION, build_enum_adapter(Params.Resolution)
        )
        """Resolution. Set with :py:class:`Params.Resolution`"""

        self.fps: BleSetting = BleSetting[Params.FPS](
            self.communicator, SettingId.FPS, build_enum_adapter(Params.FPS)
        )
        """Frames per second. Set with :py:class:`Params.FPS`"""

        self.auto_off: BleSetting = BleSetting[Params.AutoOff](
            self.communicator, SettingId.AUTO_OFF, build_enum_adapter(Params.AutoOff)
        )
        """Set the auto off time. Set with :py:class:`Params.AutoOff`"""

        self.video_field_of_view: BleSetting = BleSetting[Params.VideoFOV](
            self.communicator, SettingId.VIDEO_FOV, build_enum_adapter(Params.VideoFOV)
        )
        """Video FOV. Set with :py:class:`Params.VideoFOV`"""

        self.photo_field_of_view: BleSetting = BleSetting[Params.PhotoFOV](
            self.communicator, SettingId.PHOTO_FOV, build_enum_adapter(Params.PhotoFOV)
        )
        """Photo FOV. Set with :py:class:`Params.PhotoFOV`"""

        self.multi_shot_field_of_view: BleSetting = BleSetting[Params.MultishotFOV](
            self.communicator, SettingId.MULTI_SHOT_FOV, build_enum_adapter(Params.MultishotFOV)
        )
        """Multi-shot FOV. Set with :py:class:`Params.Multishot`"""

        self.led: BleSetting = BleSetting[Params.LED](
            self.communicator, SettingId.LED, build_enum_adapter(Params.LED)
        )
        """Set the LED options (or also send the BLE keep alive signal). Set with :py:class:`Params.LED`"""

        self.max_lens_mode: BleSetting = BleSetting[Params.MaxLensMode](
            self.communicator, SettingId.MAX_LENS_MOD, build_enum_adapter(Params.MaxLensMode)
        )
        """Enable / disable max lens mod. Set with :py:class:`Params.MaxLensMode`"""

        self.hypersmooth = BleSetting[Params.HypersmoothMode](
            self.communicator, SettingId.HYPERSMOOTH, build_enum_adapter(Params.HypersmoothMode)
        )
        """Set / disable hypersmooth. Set with :py:class:`Params.HypersmoothMode`"""

        self.video_performance_mode = BleSetting[Params.PerformanceMode](
            self.communicator,
            SettingId.VIDEO_PERFORMANCE_MODE,
            build_enum_adapter(Params.PerformanceMode),
        )
        """Video Performance Mode. Set with :py:class:`Params.PerformanceMode`"""

        self.anti_flicker = BleSetting[Params.AntiFlicker](
            self.communicator,
            SettingId.ANTI_FLICKER,
            build_enum_adapter(Params.AntiFlicker),
        )
        """Anti Flicker frequency. Set with :py:class:`Params.AntiFlicker`"""

    def __iter__(self) -> Iterator:
        """Return an iterable of this instance's attributes

        Does not include the 'communicator' attribute

        Returns:
            Iterator: next attribute
        """
        return BleSettings.Iterator(self)


class BleStatuses:
    """All of the BLE Statuses.

    To be used by a GoProBle delegate to build status commands.

    Args:
        communicator (GoProBle): Adapter to read / write settings
        params: (Type[Params]): the set of parameters to use to build the statuses
    """

    class Iterator:
        """Iterator to iterate through a BleStatuses instance's attributes

        Does not include the 'communicator' instance.
        """

        def __init__(self, statuses: "BleStatuses"):
            self._index = 0
            self._status_attributes = list(statuses.__dict__.values())[1:]  # Skip communicator

        def __next__(self) -> BleStatus:
            """Return next attribute

            Raises:
                StopIteration: Iteration has completed

            Returns:
                BleStatus: next attribute
            """
            if self._index < len(self._status_attributes):
                status = self._status_attributes[self._index]
                self._index += 1
                return status
            # End of Iteration
            raise StopIteration

    def __init__(self, communicator: GoProBle) -> None:
        self.communicator = communicator

        self.batt_present: BleStatus = BleStatus(self.communicator, StatusId.BATT_PRESENT, Flag)
        """Is the system's internal battery present?"""

        self.batt_level: BleStatus = BleStatus(self.communicator, StatusId.BATT_LEVEL, Int8ub)
        """Rough approximation of internal battery level in bars."""

        self.ext_batt_present: BleStatus = BleStatus(self.communicator, StatusId.EXT_BATT_PRESENT, Flag)
        """Is an external battery connected?"""

        self.ext_batt_level: BleStatus = BleStatus(self.communicator, StatusId.EXT_BATT_LEVEL, Int8ub)
        """External battery power level in percent."""

        self.system_hot: BleStatus = BleStatus(self.communicator, StatusId.SYSTEM_HOT, Flag)
        """Is the system currently overheating?"""

        self.system_busy: BleStatus = BleStatus(self.communicator, StatusId.SYSTEM_BUSY, Flag)
        """Is the camera busy?"""

        self.quick_capture: BleStatus = BleStatus(self.communicator, StatusId.QUICK_CAPTURE, Flag)
        """Is quick capture feature enabled?"""

        self.encoding_active: BleStatus = BleStatus(self.communicator, StatusId.ENCODING, Flag)
        """Is the camera currently encoding (i.e. capturing photo / video)?"""

        self.lcd_lock_active: BleStatus = BleStatus(self.communicator, StatusId.LCD_LOCK_ACTIVE, Flag)
        """Is the LCD lock currently active?"""

        self.video_progress: BleStatus = BleStatus(self.communicator, StatusId.VIDEO_PROGRESS, Int32ub)
        """When encoding video, this is the duration (seconds) of the video so far; 0 otherwise."""

        self.wireless_enabled: BleStatus = BleStatus(self.communicator, StatusId.WIRELESS_ENABLED, Flag)
        """Are Wireless Connections enabled?"""

        self.pair_state: BleStatus = BleStatus(
            self.communicator, StatusId.PAIR_STATE, build_enum_adapter(Params.PairState)
        )
        """What is the pair state?"""

        self.pair_type: BleStatus = BleStatus(
            self.communicator, StatusId.PAIR_TYPE, build_enum_adapter(Params.PairType)
        )
        """The last type of pairing that the camera was engaged in."""

        self.pair_time: BleStatus = BleStatus(self.communicator, StatusId.PAIR_TIME, Int32ub)
        """	Time (milliseconds) since boot of last successful pairing complete action."""

        self.wap_scan_state: BleStatus = BleStatus(
            self.communicator, StatusId.WAP_SCAN_STATE, build_enum_adapter(Params.WAPState)
        )
        """State of current scan for Wifi Access Points. Appears to only change for CAH-related scans."""

        self.wap_scan_time: BleStatus = BleStatus(self.communicator, StatusId.WAP_SCAN_TIME, Int8ub)
        """The time, in milliseconds since boot that the Wifi Access Point scan completed."""

        self.wap_prov_stat: BleStatus = BleStatus(
            self.communicator, StatusId.WAP_PROV_STAT, build_enum_adapter(Params.WAPState)
        )
        """Wifi AP provisioning state."""

        self.remote_ctrl_ver: BleStatus = BleStatus(self.communicator, StatusId.REMOTE_CTRL_VER, Int8ub)
        """What is the remote control version?"""

        self.remote_ctrl_conn: BleStatus = BleStatus(self.communicator, StatusId.REMOTE_CTRL_CONN, Flag)
        """Is the remote control connected?"""

        self.pair_state2: BleStatus = BleStatus(self.communicator, StatusId.PAIR_STATE2, Int8ub)
        """Wireless Pairing State."""

        self.wlan_ssid: BleStatus = BleStatus(
            self.communicator, StatusId.WLAN_SSID, GreedyString(encoding="utf-8")
        )
        """Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.ap_ssid: BleStatus = BleStatus(
            self.communicator, StatusId.AP_SSID, GreedyString(encoding="utf-8")
        )
        """Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.app_count: BleStatus = BleStatus(self.communicator, StatusId.APP_COUNT, Int8ub)
        """The number of wireless devices connected to the camera."""

        self.preview_enabled: BleStatus = BleStatus(self.communicator, StatusId.PREVIEW_ENABLED, Flag)
        """Is preview stream enabled?"""

        self.sd_status: BleStatus = BleStatus(
            self.communicator, StatusId.SD_STATUS, build_enum_adapter(Params.SDStatus)
        )
        """Primary Storage Status."""

        self.photos_rem: BleStatus = BleStatus(self.communicator, StatusId.PHOTOS_REM, Int32ub)
        """How many photos can be taken before sdcard is full?"""

        self.video_rem: BleStatus = BleStatus(self.communicator, StatusId.VIDEO_REM, Int32ub)
        """How many minutes of video can be captured with current settings before sdcard is full?"""

        self.num_group_photo: BleStatus = BleStatus(self.communicator, StatusId.NUM_GROUP_PHOTO, Int32ub)
        """How many group photos can be taken with current settings before sdcard is full?"""

        self.num_group_video: BleStatus = BleStatus(self.communicator, StatusId.NUM_GROUP_VIDEO, Int32ub)
        """Total number of group videos on sdcard."""

        self.num_total_photo: BleStatus = BleStatus(self.communicator, StatusId.NUM_TOTAL_PHOTO, Int32ub)
        """Total number of photos on sdcard."""

        self.num_total_video: BleStatus = BleStatus(self.communicator, StatusId.NUM_TOTAL_VIDEO, Int32ub)
        """Total number of videos on sdcard."""

        self.deprecated_40: BleStatus = BleStatus(
            self.communicator, StatusId.DEPRECATED_40, DeprecatedAdapter(GreedyString(encoding="utf-8"))
        )
        """This status is deprecated."""

        self.ota_stat: BleStatus = BleStatus(
            self.communicator, StatusId.OTA_STAT, build_enum_adapter(Params.OTAStatus)
        )
        """The current status of Over The Air (OTA) update."""

        self.download_cancel_pend: BleStatus = BleStatus(self.communicator, StatusId.DOWNLAD_CANCEL_PEND, Flag)
        """Is download firmware update cancel request pending?"""

        self.mode_group: BleStatus = BleStatus(self.communicator, StatusId.MODE_GROUP, Int8ub)
        """Current mode group (deprecated in HERO8)."""

        self.locate_active: BleStatus = BleStatus(self.communicator, StatusId.LOCATE_ACTIVE, Flag)
        """Is locate camera feature active?"""

        self.multi_count_down: BleStatus = BleStatus(self.communicator, StatusId.MULTI_COUNT_DOWN, Int32ub)
        """The current timelapse interval countdown value (e.g. 5...4...3...2...1...)."""

        self.space_rem: BleStatus = BleStatus(self.communicator, StatusId.SPACE_REM, Int64ub)
        """Remaining space on the sdcard in Kilobytes."""

        self.streaming_supp: BleStatus = BleStatus(self.communicator, StatusId.STREAMING_SUPP, Flag)
        """Is streaming supports in current recording/flatmode/secondary-stream?"""

        self.wifi_bars: BleStatus = BleStatus(self.communicator, StatusId.WIFI_BARS, Int8ub)
        """Wifi signal strength in bars."""

        self.current_time_ms: BleStatus = BleStatus(self.communicator, StatusId.CURRENT_TIME_MS, Int32ub)
        """System time in milliseconds since system was booted."""

        self.num_hilights: BleStatus = BleStatus(self.communicator, StatusId.NUM_HILIGHTS, Int8ub)
        """The number of hilights in encoding video (set to 0 when encoding stops)."""

        self.last_hilight: BleStatus = BleStatus(self.communicator, StatusId.LAST_HILIGHT, Int32ub)
        """Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)."""

        self.next_poll: BleStatus = BleStatus(self.communicator, StatusId.NEXT_POLL, Int32ub)
        """The min time between camera status updates (msec). Do not poll for status more often than this."""

        self.analytics_rdy: BleStatus = BleStatus(
            self.communicator, StatusId.ANALYTICS_RDY, build_enum_adapter(Params.AnalyticsState)
        )
        """The current state of camera analytics."""

        self.analytics_size: BleStatus = BleStatus(self.communicator, StatusId.ANALYTICS_SIZE, Int32ub)
        """The size (units??) of the analytics file."""

        self.in_context_menu: BleStatus = BleStatus(self.communicator, StatusId.IN_CONTEXT_MENU, Flag)
        """Is the camera currently in a contextual menu (e.g. Preferences)?"""

        self.timelapse_rem: BleStatus = BleStatus(self.communicator, StatusId.TIMELAPSE_REM, Int32ub)
        """How many min of Timelapse video can be captured with current settings before sdcard is full?"""

        self.exposure_type: BleStatus = BleStatus(
            self.communicator, StatusId.EXPOSURE_TYPE, build_enum_adapter(Params.ExposureMode)
        )
        """Liveview Exposure Select Mode."""

        self.exposure_x: BleStatus = BleStatus(self.communicator, StatusId.EXPOSURE_X, Int8ub)
        """Liveview Exposure Select: y-coordinate (percent)."""

        self.exposure_y: BleStatus = BleStatus(self.communicator, StatusId.EXPOSURE_Y, Int8ub)
        """Liveview Exposure Select: y-coordinate (percent)."""

        self.gps_stat: BleStatus = BleStatus(self.communicator, StatusId.GPS_STAT, Flag)
        """Does the camera currently have a GPS lock?"""

        self.ap_state: BleStatus = BleStatus(self.communicator, StatusId.AP_STATE, Flag)
        """Is the Wifi radio enabled?"""

        self.int_batt_per: BleStatus = BleStatus(self.communicator, StatusId.INT_BATT_PER, Int8ub)
        """Internal battery level (percent)."""

        self.acc_mic_stat: BleStatus = BleStatus(
            self.communicator, StatusId.ACC_MIC_STAT, build_enum_adapter(Params.ExposureMode)
        )
        """Microphone Accesstory status."""

        self.digital_zoom: BleStatus = BleStatus(self.communicator, StatusId.DIGITAL_ZOOM, Int8ub)
        """	Digital Zoom level (percent)."""

        self.wireless_band: BleStatus = BleStatus(
            self.communicator, StatusId.WIRELESS_BAND, build_enum_adapter(Params.WifiBand)
        )
        """Wireless Band."""

        self.dig_zoom_active: BleStatus = BleStatus(self.communicator, StatusId.DIG_ZOOM_ACTIVE, Flag)
        """Is Digital Zoom feature available?"""

        self.mobile_video: BleStatus = BleStatus(self.communicator, StatusId.MOBILE_VIDEO, Flag)
        """Are current video settings mobile friendly? (related to video compression and frame rate)."""

        self.first_time: BleStatus = BleStatus(self.communicator, StatusId.FIRST_TIME, Flag)
        """Is the camera currently in First Time Use (FTU) UI flow?"""

        self.sec_sd_stat: BleStatus = BleStatus(
            self.communicator, StatusId.SEC_SD_STAT, build_enum_adapter(Params.SDStatus)
        )
        """Secondary Storage Status (exclusive to Superbank)."""

        self.band_5ghz_avail: BleStatus = BleStatus(self.communicator, StatusId.BAND_5GHZ_AVAIL, Flag)
        """Is 5GHz wireless band available?"""

        self.system_ready: BleStatus = BleStatus(self.communicator, StatusId.SYSTEM_READY, Flag)
        """Is the system ready to accept commands?"""

        self.batt_ok_ota: BleStatus = BleStatus(self.communicator, StatusId.BATT_OK_OTA, Flag)
        """Is the internal battery charged sufficiently to start Over The Air (OTA) update?"""

        self.video_low_temp: BleStatus = BleStatus(self.communicator, StatusId.VIDEO_LOW_TEMP, Flag)
        """Is the camera getting too cold to continue recording?"""

        self.orientation: BleStatus = BleStatus(
            self.communicator, StatusId.ORIENTATION, build_enum_adapter(Params.Orientation)
        )
        """The rotational orientation of the camera."""

        self.thermal_mit_mode: BleStatus = BleStatus(self.communicator, StatusId.THERMAL_MIT_MODE, Flag)
        """Can camera use high resolution/fps (based on temperature)?"""

        self.zoom_encoding: BleStatus = BleStatus(self.communicator, StatusId.ZOOM_ENCODING, Flag)
        """Is this camera capable of zooming while encoding (static value based on model, not settings)?"""

        self.flatmode_id: BleStatus = BleStatus(
            self.communicator, StatusId.FLATMODE_ID, build_enum_adapter(Params.Flatmode)
        )
        """Current flatmode ID."""

        self.logs_ready: BleStatus = BleStatus(self.communicator, StatusId.LOGS_READY, Flag)
        """	Are system logs ready to be downloaded?"""

        self.deprecated_92: BleStatus = BleStatus(
            self.communicator, StatusId.DEPRECATED_92, DeprecatedAdapter(Flag)
        )
        """This status is deprecated."""

        self.video_presets: BleStatus = BleStatus(self.communicator, StatusId.VIDEO_PRESETS, Int32ub)
        """Current Video Preset (ID)."""

        self.photo_presets: BleStatus = BleStatus(self.communicator, StatusId.PHOTO_PRESETS, Int32ub)
        """Current Photo Preset (ID)."""

        self.timelapse_presets: BleStatus = BleStatus(self.communicator, StatusId.TIMELAPSE_PRESETS, Int32ub)
        """	Current Timelapse Preset (ID)."""

        self.presets_group: BleStatus = BleStatus(self.communicator, StatusId.PRESETS_GROUP, Int32ub)
        """Current Preset Group (ID)."""

        self.active_preset: BleStatus = BleStatus(self.communicator, StatusId.ACTIVE_PRESET, Int32ub)
        """Currently Preset (ID)."""

        self.preset_modified: BleStatus = BleStatus(self.communicator, StatusId.PRESET_MODIFIED, Int32ub)
        """Preset Modified Status, which contains an event ID and a preset (group) ID."""

        self.live_burst_rem: BleStatus = BleStatus(self.communicator, StatusId.LIVE_BURST_REM, Int32ub)
        """How many Live Bursts can be captured before sdcard is full?"""

        self.live_burst_total: BleStatus = BleStatus(self.communicator, StatusId.LIVE_BURST_TOTAL, Int32ub)
        """Total number of Live Bursts on sdcard."""

        self.capt_delay_active: BleStatus = BleStatus(self.communicator, StatusId.CAPT_DELAY_ACTIVE, Flag)
        """Is Capture Delay currently active (i.e. counting down)?"""

        self.media_mod_mic_stat: BleStatus = BleStatus(
            self.communicator,
            StatusId.MEDIA_MOD_MIC_STAT,
            build_enum_adapter(Params.MediaModMicStatus),
        )
        """Media mod State."""

        self.timewarp_speed_ramp: BleStatus = BleStatus(
            self.communicator, StatusId.TIMEWARP_SPEED_RAMP, build_enum_adapter(Params.TimeWarpSpeed)
        )
        """Time Warp Speed."""

        self.linux_core_active: BleStatus = BleStatus(self.communicator, StatusId.LINUX_CORE_ACTIVE, Flag)
        """Is the system's Linux core active?"""

        self.camera_lens_type: BleStatus = BleStatus(
            self.communicator, StatusId.CAMERA_LENS_TYPE, build_enum_adapter(Params.MaxLensMode)
        )
        """Camera lens type (reflects changes to setting 162)."""

        self.video_hindsight: BleStatus = BleStatus(self.communicator, StatusId.VIDEO_HINDSIGHT, Flag)
        """Is Video Hindsight Capture Active?"""

        self.scheduled_preset: BleStatus = BleStatus(self.communicator, StatusId.SCHEDULED_PRESET, Int32ub)
        """Scheduled Capture Preset ID."""

        self.scheduled_capture: BleStatus = BleStatus(self.communicator, StatusId.SCHEDULED_CAPTURE, Flag)
        """Is Scheduled Capture set?"""

        self.creating_preset: BleStatus = BleStatus(self.communicator, StatusId.CREATING_PRESET, Flag)
        """Is the camera in the process of creating a custom preset?"""

        self.media_mod_stat: BleStatus = BleStatus(
            self.communicator, StatusId.MEDIA_MOD_STAT, build_enum_adapter(Params.MediaModStatus)
        )
        """Media Mode Status (bitmasked)."""

        self.turbo_mode: BleStatus = BleStatus(self.communicator, StatusId.TURBO_MODE, Flag)
        """Is Turbo Transfer active?"""

        self.sd_rating_check_error: BleStatus = BleStatus(
            self.communicator, StatusId.SD_RATING_CHECK_ERROR, Flag
        )
        """Does sdcard meet specified minimum write speed?"""

        self.sd_write_speed_error: BleStatus = BleStatus(
            self.communicator, StatusId.SD_WRITE_SPEED_ERROR, Int8ub
        )
        """Number of sdcard write speed errors since device booted"""

        self.camera_control: BleStatus = BleStatus(
            self.communicator, StatusId.CAMERA_CONTROL, build_enum_adapter(Params.CameraControlStatus)
        )
        """Camera control status ID"""

        self.usb_connected: BleStatus = BleStatus(self.communicator, StatusId.USB_CONNECTED, Flag)
        """Is the camera connected to a PC via USB?"""

        self.control_allowed_over_usb: BleStatus = BleStatus(
            self.communicator, StatusId.CONTROL_OVER_USB, Flag
        )
        """Is control allowed over USB?"""

    def __iter__(self) -> Iterator:
        """Return an iterable of this instance's attributes

        Does not include the 'communicator' attribute

        Returns:
            Iterator: next attribute
        """
        return BleStatuses.Iterator(self)
