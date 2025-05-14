# ble_statuses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 20 23:24:52 UTC 2025

"""BLE Statuses"""

########################################################################################################################
#
# Warning!! This file is auto-generated. Do not modify it manually.
#
########################################################################################################################

from construct import Flag, GreedyString, Int8ub, Int32ub, Int64ub

from open_gopro.api.builders import BleStatusFacade as BleStatus
from open_gopro.domain.communicator_interface import BleMessages, GoProBle
from open_gopro.models.constants import StatusId
from open_gopro.models.constants.statuses import *  # pylint: disable = wildcard-import, unused-wildcard-import


class BleStatuses(BleMessages[BleStatus.BleStatusMessageBase]):
    """All of the BLE Statuses.

    To be used by a GoProBle delegate to build status messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProBle) -> None:

        self.battery_present: BleStatus[bool] = BleStatus(communicator, StatusId.BATTERY_PRESENT, Flag)
        """Battery Present

        Is the system's internal battery present?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#battery-present-1)"""

        self.internal_battery_bars: BleStatus[InternalBatteryBars] = BleStatus(
            communicator, StatusId.INTERNAL_BATTERY_BARS, InternalBatteryBars
        )
        """Internal Battery Bars

        Rough approximation of internal battery level in bars (or charging)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-bars-2)"""

        self.overheating: BleStatus[bool] = BleStatus(communicator, StatusId.OVERHEATING, Flag)
        """Overheating

        Is the system currently overheating?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#overheating-6)"""

        self.busy: BleStatus[bool] = BleStatus(communicator, StatusId.BUSY, Flag)
        """Busy

        Is the camera busy?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8)"""

        self.quick_capture: BleStatus[bool] = BleStatus(communicator, StatusId.QUICK_CAPTURE, Flag)
        """Quick Capture

        Is Quick Capture feature enabled?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#quick-capture-9)"""

        self.encoding: BleStatus[bool] = BleStatus(communicator, StatusId.ENCODING, Flag)
        """Encoding

        Is the system currently encoding?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10)"""

        self.lcd_lock: BleStatus[bool] = BleStatus(communicator, StatusId.LCD_LOCK, Flag)
        """LCD Lock

        Is LCD lock active?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lcd-lock-11)"""

        self.video_encoding_duration: BleStatus[int] = BleStatus(
            communicator, StatusId.VIDEO_ENCODING_DURATION, Int32ub
        )
        """Video Encoding Duration

        When encoding video, this is the duration (seconds) of the video so far; 0 otherwise

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-encoding-duration-13)"""

        self.wireless_connections_enabled: BleStatus[bool] = BleStatus(
            communicator, StatusId.WIRELESS_CONNECTIONS_ENABLED, Flag
        )
        """Wireless Connections Enabled

        Are Wireless Connections enabled?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-connections-enabled-17)"""

        self.pairing_state: BleStatus[PairingState] = BleStatus(communicator, StatusId.PAIRING_STATE, PairingState)
        """Pairing State

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-19)"""

        self.last_pairing_type: BleStatus[LastPairingType] = BleStatus(
            communicator, StatusId.LAST_PAIRING_TYPE, LastPairingType
        )
        """Last Pairing Type

        The last type of pairing in which the camera was engaged

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-type-20)"""

        self.last_pairing_success: BleStatus[int] = BleStatus(communicator, StatusId.LAST_PAIRING_SUCCESS, Int32ub)
        """Last Pairing Success

        Time since boot (milliseconds) of last successful pairing complete action

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-success-21)"""

        self.wifi_scan_state: BleStatus[WifiScanState] = BleStatus(
            communicator, StatusId.WIFI_SCAN_STATE, WifiScanState
        )
        """Wifi Scan State

        State of current scan for WiFi Access Points

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-scan-state-22)"""

        self.last_wifi_scan_success: BleStatus[int] = BleStatus(communicator, StatusId.LAST_WIFI_SCAN_SUCCESS, Int8ub)
        """Last Wifi Scan Success

        Time since boot (milliseconds) that the WiFi Access Point scan completed

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-wifi-scan-success-23)"""

        self.wifi_provisioning_state: BleStatus[WifiProvisioningState] = BleStatus(
            communicator, StatusId.WIFI_PROVISIONING_STATE, WifiProvisioningState
        )
        """Wifi Provisioning State

        WiFi AP provisioning state

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-provisioning-state-24)"""

        self.remote_version: BleStatus[int] = BleStatus(communicator, StatusId.REMOTE_VERSION, Int8ub)
        """Remote Version

        Wireless remote control version

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-version-26)"""

        self.remote_connected: BleStatus[bool] = BleStatus(communicator, StatusId.REMOTE_CONNECTED, Flag)
        """Remote Connected

        Is a wireless remote control connected?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-connected-27)"""

        self.connected_wifi_ssid: BleStatus[str] = BleStatus(
            communicator, StatusId.CONNECTED_WIFI_SSID, GreedyString(encoding="utf-8")
        )
        """Connected WiFi SSID

        The name of the wireless network that the camera is connected to where the camera is acting as a client/station.
		
		When read via BLE, this value is big-endian byte-encoded int32.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#connected-wifi-ssid-29)"""

        self.access_point_ssid: BleStatus[str] = BleStatus(
            communicator, StatusId.ACCESS_POINT_SSID, GreedyString(encoding="utf-8")
        )
        """Access Point SSID

        The name of the network that the camera sets up in AP mode for other devices to connect to.
		
		When read via BLE, this value is big-endian byte-encoded int32.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#access-point-ssid-30)"""

        self.connected_devices: BleStatus[int] = BleStatus(communicator, StatusId.CONNECTED_DEVICES, Int8ub)
        """Connected Devices

        The number of wireless devices connected to the camera

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#connected-devices-31)"""

        self.preview_stream: BleStatus[bool] = BleStatus(communicator, StatusId.PREVIEW_STREAM, Flag)
        """Preview Stream

        Is Preview Stream enabled?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-32)"""

        self.primary_storage: BleStatus[PrimaryStorage] = BleStatus(
            communicator, StatusId.PRIMARY_STORAGE, PrimaryStorage
        )
        """Primary Storage

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#primary-storage-33)"""

        self.remaining_photos: BleStatus[int] = BleStatus(communicator, StatusId.REMAINING_PHOTOS, Int32ub)
        """Remaining Photos

        How many photos can be taken with current settings before sdcard is full.
		
		Alternatively, this is:
		
		- the remaining timelapse capability if Setting 128 is set to Timelapse Photo
		- the remaining nightlapse capability if Setting 128 is set to Nightlapse Photo

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-photos-34)"""

        self.remaining_video_time: BleStatus[int] = BleStatus(communicator, StatusId.REMAINING_VIDEO_TIME, Int32ub)
        """Remaining Video Time

        How many seconds of video can be captured with current settings before sdcard is full
		
		Alternatively, this is:
		
		- the remaining timelapse capability if Setting 128 is set to Timelapse Video
		- the remaining nightlapse capability if Setting 128 is set to Nightlapse Video

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-video-time-35)"""

        self.photos: BleStatus[int] = BleStatus(communicator, StatusId.PHOTOS, Int32ub)
        """Photos

        Total number of photos on sdcard

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photos-38)"""

        self.videos: BleStatus[int] = BleStatus(communicator, StatusId.VIDEOS, Int32ub)
        """Videos

        Total number of videos on sdcard

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#videos-39)"""

        self.ota: BleStatus[Ota] = BleStatus(communicator, StatusId.OTA, Ota)
        """OTA

        The current status of Over The Air (OTA) update

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-41)"""

        self.pending_fw_update_cancel: BleStatus[bool] = BleStatus(
            communicator, StatusId.PENDING_FW_UPDATE_CANCEL, Flag
        )
        """Pending FW Update Cancel

        Is there a pending request to cancel a firmware update download?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pending-fw-update-cancel-42)"""

        self.locate: BleStatus[bool] = BleStatus(communicator, StatusId.LOCATE, Flag)
        """Locate

        Is locate camera feature active?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#locate-45)"""

        self.timelapse_interval_countdown: BleStatus[int] = BleStatus(
            communicator, StatusId.TIMELAPSE_INTERVAL_COUNTDOWN, Int32ub
        )
        """Timelapse Interval Countdown

        The current timelapse interval countdown value (e.g. 5...4...3...2...1...)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-interval-countdown-49)"""

        self.sd_card_remaining: BleStatus[int] = BleStatus(communicator, StatusId.SD_CARD_REMAINING, Int64ub)
        """SD Card Remaining

        Remaining space on the sdcard in Kilobytes

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-remaining-54)"""

        self.preview_stream_available: BleStatus[bool] = BleStatus(
            communicator, StatusId.PREVIEW_STREAM_AVAILABLE, Flag
        )
        """Preview Stream Available

        Is preview stream supported in current recording/mode/secondary-stream?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-available-55)"""

        self.wifi_bars: BleStatus[int] = BleStatus(communicator, StatusId.WIFI_BARS, Int8ub)
        """Wifi Bars

        WiFi signal strength in bars

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-bars-56)"""

        self.active_hilights: BleStatus[int] = BleStatus(communicator, StatusId.ACTIVE_HILIGHTS, Int8ub)
        """Active Hilights

        The number of hilights in currently-encoding video (value is set to 0 when encoding stops)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#active-hilights-58)"""

        self.time_since_last_hilight: BleStatus[int] = BleStatus(
            communicator, StatusId.TIME_SINCE_LAST_HILIGHT, Int32ub
        )
        """Time Since Last Hilight

        Time since boot (milliseconds) of most recent hilight in encoding video (set to 0 when encoding stops)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-since-last-hilight-59)"""

        self.minimum_status_poll_period: BleStatus[int] = BleStatus(
            communicator, StatusId.MINIMUM_STATUS_POLL_PERIOD, Int32ub
        )
        """Minimum Status Poll Period

        The minimum time between camera status updates (milliseconds). Best practice is to not poll for status more
		often than this

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#minimum-status-poll-period-60)"""

        self.liveview_exposure_select_mode: BleStatus[LiveviewExposureSelectMode] = BleStatus(
            communicator, StatusId.LIVEVIEW_EXPOSURE_SELECT_MODE, LiveviewExposureSelectMode
        )
        """Liveview Exposure Select Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-exposure-select-mode-65)"""

        self.liveview_y: BleStatus[int] = BleStatus(communicator, StatusId.LIVEVIEW_Y, Int8ub)
        """Liveview Y

        Liveview Exposure Select: y-coordinate (percent)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-y-66)"""

        self.liveview_x: BleStatus[int] = BleStatus(communicator, StatusId.LIVEVIEW_X, Int8ub)
        """Liveview X

        Liveview Exposure Select: y-coordinate (percent)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-x-67)"""

        self.gps_lock: BleStatus[bool] = BleStatus(communicator, StatusId.GPS_LOCK, Flag)
        """GPS Lock

        Does the camera currently have a GPS lock?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#gps-lock-68)"""

        self.ap_mode: BleStatus[bool] = BleStatus(communicator, StatusId.AP_MODE, Flag)
        """AP Mode

        Is AP mode enabled?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ap-mode-69)"""

        self.internal_battery_percentage: BleStatus[int] = BleStatus(
            communicator, StatusId.INTERNAL_BATTERY_PERCENTAGE, Int8ub
        )
        """Internal Battery Percentage

        Internal battery level as percentage

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-percentage-70)"""

        self.microphone_accessory: BleStatus[MicrophoneAccessory] = BleStatus(
            communicator, StatusId.MICROPHONE_ACCESSORY, MicrophoneAccessory
        )
        """Microphone Accessory

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#microphone-accessory-74)"""

        self.zoom_level: BleStatus[int] = BleStatus(communicator, StatusId.ZOOM_LEVEL, Int8ub)
        """Zoom Level

        Digital Zoom level as percentage

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-level-75)"""

        self.wireless_band: BleStatus[WirelessBand] = BleStatus(communicator, StatusId.WIRELESS_BAND, WirelessBand)
        """Wireless Band

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-band-76)"""

        self.zoom_available: BleStatus[bool] = BleStatus(communicator, StatusId.ZOOM_AVAILABLE, Flag)
        """Zoom Available

        Is Digital Zoom feature available?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-available-77)"""

        self.mobile_friendly: BleStatus[bool] = BleStatus(communicator, StatusId.MOBILE_FRIENDLY, Flag)
        """Mobile Friendly

        Are current video settings mobile friendly? (related to video compression and frame rate)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#mobile-friendly-78)"""

        self.ftu: BleStatus[bool] = BleStatus(communicator, StatusId.FTU, Flag)
        """FTU

        Is the camera currently in First Time Use (FTU) UI flow?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ftu-79)"""

        self.num_5ghz_available: BleStatus[bool] = BleStatus(communicator, StatusId.NUM_5GHZ_AVAILABLE, Flag)
        """5GHZ Available

        Is 5GHz wireless band available?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#5ghz-available-81)"""

        self.ready: BleStatus[bool] = BleStatus(communicator, StatusId.READY, Flag)
        """Ready

        Is the system fully booted and ready to accept commands?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ready-82)"""

        self.ota_charged: BleStatus[bool] = BleStatus(communicator, StatusId.OTA_CHARGED, Flag)
        """OTA Charged

        Is the internal battery charged sufficiently to start Over The Air (OTA) update?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-charged-83)"""

        self.cold: BleStatus[bool] = BleStatus(communicator, StatusId.COLD, Flag)
        """Cold

        Is the camera getting too cold to continue recording?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#cold-85)"""

        self.rotation: BleStatus[Rotation] = BleStatus(communicator, StatusId.ROTATION, Rotation)
        """Rotation

        Rotational orientation of the camera

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#rotation-86)"""

        self.zoom_while_encoding: BleStatus[bool] = BleStatus(communicator, StatusId.ZOOM_WHILE_ENCODING, Flag)
        """Zoom while Encoding

        Is this camera model capable of zooming while encoding?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-while-encoding-88)"""

        self.flatmode: BleStatus[int] = BleStatus(communicator, StatusId.FLATMODE, Int8ub)
        """Flatmode

        Current Flatmode ID

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#flatmode-89)"""

        self.video_preset: BleStatus[int] = BleStatus(communicator, StatusId.VIDEO_PRESET, Int32ub)
        """Video Preset

        Current Video Preset (ID)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-preset-93)"""

        self.photo_preset: BleStatus[int] = BleStatus(communicator, StatusId.PHOTO_PRESET, Int32ub)
        """Photo Preset

        Current Photo Preset (ID)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-preset-94)"""

        self.timelapse_preset: BleStatus[int] = BleStatus(communicator, StatusId.TIMELAPSE_PRESET, Int32ub)
        """Timelapse Preset

        Current Time Lapse Preset (ID)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-preset-95)"""

        self.preset_group: BleStatus[int] = BleStatus(communicator, StatusId.PRESET_GROUP, Int32ub)
        """Preset Group

        Current Preset Group (ID) (corresponds to ui_mode_groups in settings.json)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-group-96)"""

        self.preset: BleStatus[int] = BleStatus(communicator, StatusId.PRESET, Int32ub)
        """Preset

        Current Preset (ID)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-97)"""

        self.preset_modified: BleStatus[int] = BleStatus(communicator, StatusId.PRESET_MODIFIED, Int32ub)
        """Preset Modified

        The value of this status is set to zero when the client sends a Get Preset Status message to the camera.
		
		The value of this status is set to a non-zero value when:
		
		- Preset settings submenu is exited in the camera UI (whether any settings were changed or not)
		- A new preset is created
		- A preset is deleted
		- Preset ordering is changed within a preset group
		- A preset is reset to factory defaults

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-modified-98)"""

        self.remaining_live_bursts: BleStatus[int] = BleStatus(communicator, StatusId.REMAINING_LIVE_BURSTS, Int32ub)
        """Remaining Live Bursts

        The number of Live Bursts can be captured with current settings before sdcard is full

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-live-bursts-99)"""

        self.live_bursts: BleStatus[int] = BleStatus(communicator, StatusId.LIVE_BURSTS, Int32ub)
        """Live Bursts

        Total number of Live Bursts on sdcard

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#live-bursts-100)"""

        self.capture_delay_active: BleStatus[bool] = BleStatus(communicator, StatusId.CAPTURE_DELAY_ACTIVE, Flag)
        """Capture Delay Active

        Is Capture Delay currently active (i.e. counting down)?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#capture-delay-active-101)"""

        self.media_mod_state: BleStatus[MediaModState] = BleStatus(
            communicator, StatusId.MEDIA_MOD_STATE, MediaModState
        )
        """Media Mod State

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#media-mod-state-102)"""

        self.time_warp_speed: BleStatus[TimeWarpSpeed] = BleStatus(
            communicator, StatusId.TIME_WARP_SPEED, TimeWarpSpeed
        )
        """Time Warp Speed

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-warp-speed-103)"""

        self.linux_core: BleStatus[bool] = BleStatus(communicator, StatusId.LINUX_CORE, Flag)
        """Linux Core

        Is the system's Linux core active?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#linux-core-104)"""

        self.lens_type: BleStatus[LensType] = BleStatus(communicator, StatusId.LENS_TYPE, LensType)
        """Lens Type

        Camera lens type (reflects changes to lens settings such as 162, 189, 194, ...)

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lens-type-105)"""

        self.hindsight: BleStatus[bool] = BleStatus(communicator, StatusId.HINDSIGHT, Flag)
        """Hindsight

        Is Video Hindsight Capture Active?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#hindsight-106)"""

        self.scheduled_capture_preset_id: BleStatus[int] = BleStatus(
            communicator, StatusId.SCHEDULED_CAPTURE_PRESET_ID, Int32ub
        )
        """Scheduled Capture Preset ID

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-preset-id-107)"""

        self.scheduled_capture: BleStatus[bool] = BleStatus(communicator, StatusId.SCHEDULED_CAPTURE, Flag)
        """Scheduled Capture

        Is Scheduled Capture set?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-108)"""

        self.display_mod_status: BleStatus[DisplayModStatus] = BleStatus(
            communicator, StatusId.DISPLAY_MOD_STATUS, DisplayModStatus
        )
        """Display Mod Status

        Note that this is a bitmasked value.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#display-mod-status-110)"""

        self.sd_card_write_speed_error: BleStatus[bool] = BleStatus(
            communicator, StatusId.SD_CARD_WRITE_SPEED_ERROR, Flag
        )
        """SD Card Write Speed Error

        Is there an SD Card minimum write speed error?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-write-speed-error-111)"""

        self.sd_card_errors: BleStatus[int] = BleStatus(communicator, StatusId.SD_CARD_ERRORS, Int8ub)
        """SD Card Errors

        Number of sdcard write speed errors since device booted

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-errors-112)"""

        self.turbo_transfer: BleStatus[bool] = BleStatus(communicator, StatusId.TURBO_TRANSFER, Flag)
        """Turbo Transfer

        Is Turbo Transfer active?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#turbo-transfer-113)"""

        self.camera_control_id: BleStatus[CameraControlId] = BleStatus(
            communicator, StatusId.CAMERA_CONTROL_ID, CameraControlId
        )
        """Camera Control ID

        Camera control status ID

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-control-id-114)"""

        self.usb_connected: BleStatus[bool] = BleStatus(communicator, StatusId.USB_CONNECTED, Flag)
        """USB Connected

        Is the camera connected to a PC via USB?

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-connected-115)"""

        self.usb_controlled: BleStatus[UsbControlled] = BleStatus(communicator, StatusId.USB_CONTROLLED, UsbControlled)
        """USB Controlled

        Camera control over USB state

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-controlled-116)"""

        self.sd_card_capacity: BleStatus[int] = BleStatus(communicator, StatusId.SD_CARD_CAPACITY, Int32ub)
        """SD Card Capacity

        Total SD card capacity in Kilobytes

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-capacity-117)"""

        self.photo_interval_capture_count: BleStatus[int] = BleStatus(
            communicator, StatusId.PHOTO_INTERVAL_CAPTURE_COUNT, Int32ub
        )
        """Photo Interval Capture Count

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-interval-capture-count-118)"""

        super().__init__(communicator)
