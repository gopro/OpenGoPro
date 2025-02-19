"""BLE Statuses"""

from typing import Any

from construct import Flag, GreedyString, Int8ub, Int32ub, Int64ub

from open_gopro.api.builders import BleStatusFacade as BleStatus
from open_gopro.api.parsers import ByteParserBuilders
from open_gopro.communicator_interface import BleMessages, GoProBle
from open_gopro.constants import StatusId

from . import Params


class BleStatuses(BleMessages[BleStatus.BleStatusMessageBase]):
    """All of the BLE Statuses.

    To be used by a GoProBle delegate to build status messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProBle) -> None:
        self.batt_present: BleStatus[bool] = BleStatus(communicator, StatusId.BATT_PRESENT, Flag)
        """Is the system's internal battery present?"""

        self.batt_level: BleStatus[int] = BleStatus(communicator, StatusId.BATT_LEVEL, Int8ub)
        """Rough approximation of internal battery level in bars."""

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
        """Secondary Storage Status"""

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

        self.photo_interval_capture_count: BleStatus[int] = BleStatus(
            communicator, StatusId.PHOTO_INTERVAL_CAPTURE_COUNT, Int32ub
        )
        """Photo interval capture count"""

        self.camera_lens_mod: BleStatus[Params.LensModStatus] = BleStatus(
            communicator, StatusId.CAMERA_LENS_MOD, Params.LensModStatus
        )
        """Current camera lens mod"""

        super().__init__(communicator)
