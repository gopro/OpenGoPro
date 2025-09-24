/* StatusesContainer.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu Feb 20 23:24:56 UTC 2025 */

package com.gopro.open_gopro.gopro

/**
 * *********************************************************************************************************
 *
 * WARNING!!! This file is auto-generated. Do not modify it manually
 */
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.operations.*
import com.gopro.open_gopro.util.extensions.decodeToString
import com.gopro.open_gopro.util.extensions.toBoolean

@OptIn(ExperimentalUnsignedTypes::class)
private fun toBoolean(data: UByteArray): Boolean = data.last().toBoolean()

@OptIn(ExperimentalUnsignedTypes::class)
private fun toInt8(data: UByteArray): Int = data.last().toInt()

@OptIn(ExperimentalUnsignedTypes::class)
private fun toString(data: UByteArray): String = data.decodeToString()

/**
 * Container used to access and operate on statuses.
 *
 * @param marshaller
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html)
 */
@OptIn(ExperimentalUnsignedTypes::class)
class StatusesContainer internal constructor(marshaller: IOperationMarshaller) {

  /**
   * Battery Present
   *
   * Is the system's internal battery present?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#battery-present-1)
   */
  val batteryPresent = Status(StatusId.BATTERY_PRESENT, marshaller, ::toBoolean)

  /**
   * Internal Battery Bars
   *
   * Rough approximation of internal battery level in bars (or charging)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-bars-2)
   */
  val internalBatteryBars = Status(StatusId.INTERNAL_BATTERY_BARS, marshaller, ::toInt8)

  /**
   * Overheating
   *
   * Is the system currently overheating?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#overheating-6)
   */
  val overheating = Status(StatusId.OVERHEATING, marshaller, ::toBoolean)

  /**
   * Busy
   *
   * Is the camera busy?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8)
   */
  val busy = Status(StatusId.BUSY, marshaller, ::toBoolean)

  /**
   * Quick Capture
   *
   * Is Quick Capture feature enabled?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#quick-capture-9)
   */
  val quickCapture = Status(StatusId.QUICK_CAPTURE, marshaller, ::toBoolean)

  /**
   * Encoding
   *
   * Is the system currently encoding?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10)
   */
  val encoding = Status(StatusId.ENCODING, marshaller, ::toBoolean)

  /**
   * LCD Lock
   *
   * Is LCD lock active?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lcd-lock-11)
   */
  val lcdLock = Status(StatusId.LCD_LOCK, marshaller, ::toBoolean)

  /**
   * Video Encoding Duration
   *
   * When encoding video, this is the duration (seconds) of the video so far; 0 otherwise
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-encoding-duration-13)
   */
  val videoEncodingDuration = Status(StatusId.VIDEO_ENCODING_DURATION, marshaller, ::toInt8)

  /**
   * Wireless Connections Enabled
   *
   * Are Wireless Connections enabled?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-connections-enabled-17)
   */
  val wirelessConnectionsEnabled =
      Status(StatusId.WIRELESS_CONNECTIONS_ENABLED, marshaller, ::toBoolean)

  /**
   * Pairing State
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-19)
   */
  val pairingState = Status(StatusId.PAIRING_STATE, marshaller, ::toInt8)

  /**
   * Last Pairing Type
   *
   * The last type of pairing in which the camera was engaged
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-type-20)
   */
  val lastPairingType = Status(StatusId.LAST_PAIRING_TYPE, marshaller, ::toInt8)

  /**
   * Last Pairing Success
   *
   * Time since boot (milliseconds) of last successful pairing complete action
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-success-21)
   */
  val lastPairingSuccess = Status(StatusId.LAST_PAIRING_SUCCESS, marshaller, ::toInt8)

  /**
   * Wifi Scan State
   *
   * State of current scan for WiFi Access Points
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-scan-state-22)
   */
  val wifiScanState = Status(StatusId.WIFI_SCAN_STATE, marshaller, ::toInt8)

  /**
   * Last Wifi Scan Success
   *
   * Time since boot (milliseconds) that the WiFi Access Point scan completed
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-wifi-scan-success-23)
   */
  val lastWifiScanSuccess = Status(StatusId.LAST_WIFI_SCAN_SUCCESS, marshaller, ::toInt8)

  /**
   * Wifi Provisioning State
   *
   * WiFi AP provisioning state
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-provisioning-state-24)
   */
  val wifiProvisioningState = Status(StatusId.WIFI_PROVISIONING_STATE, marshaller, ::toInt8)

  /**
   * Remote Version
   *
   * Wireless remote control version
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-version-26)
   */
  val remoteVersion = Status(StatusId.REMOTE_VERSION, marshaller, ::toInt8)

  /**
   * Remote Connected
   *
   * Is a wireless remote control connected?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-connected-27)
   */
  val remoteConnected = Status(StatusId.REMOTE_CONNECTED, marshaller, ::toBoolean)

  /**
   * Pairing State (Legacy)
   *
   * Wireless Pairing State. Each bit contains state information (see WirelessPairingStateFlags)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-(legacy)-28)
   */
  val pairingState_Legacy_ = Status(StatusId.PAIRING_STATE_LEGACY_, marshaller, ::toInt8)

  /**
   * Connected WiFi SSID
   *
   * The name of the wireless network that the camera is connected to where the camera is acting as
   * a client/station.
   *
   * When read via BLE, this value is big-endian byte-encoded int32.
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#connected-wifi-ssid-29)
   */
  val connectedWifiSsid = Status(StatusId.CONNECTED_WIFI_SSID, marshaller, ::toString)

  /**
   * Access Point SSID
   *
   * The name of the network that the camera sets up in AP mode for other devices to connect to.
   *
   * When read via BLE, this value is big-endian byte-encoded int32.
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#access-point-ssid-30)
   */
  val accessPointSsid = Status(StatusId.ACCESS_POINT_SSID, marshaller, ::toString)

  /**
   * Connected Devices
   *
   * The number of wireless devices connected to the camera
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#connected-devices-31)
   */
  val connectedDevices = Status(StatusId.CONNECTED_DEVICES, marshaller, ::toInt8)

  /**
   * Preview Stream
   *
   * Is Preview Stream enabled?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-32)
   */
  val previewStream = Status(StatusId.PREVIEW_STREAM, marshaller, ::toBoolean)

  /**
   * Primary Storage
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#primary-storage-33)
   */
  val primaryStorage = Status(StatusId.PRIMARY_STORAGE, marshaller, ::toInt8)

  /**
   * Remaining Photos
   *
   * How many photos can be taken with current settings before sdcard is full.
   *
   * Alternatively, this is:
   * - the remaining timelapse capability if Setting 128 is set to Timelapse Photo
   * - the remaining nightlapse capability if Setting 128 is set to Nightlapse Photo
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-photos-34)
   */
  val remainingPhotos = Status(StatusId.REMAINING_PHOTOS, marshaller, ::toInt8)

  /**
   * Remaining Video Time
   *
   * How many seconds of video can be captured with current settings before sdcard is full
   *
   * Alternatively, this is:
   * - the remaining timelapse capability if Setting 128 is set to Timelapse Video
   * - the remaining nightlapse capability if Setting 128 is set to Nightlapse Video
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-video-time-35)
   */
  val remainingVideoTime = Status(StatusId.REMAINING_VIDEO_TIME, marshaller, ::toInt8)

  /**
   * Photos
   *
   * Total number of photos on sdcard
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photos-38)
   */
  val photos = Status(StatusId.PHOTOS, marshaller, ::toInt8)

  /**
   * Videos
   *
   * Total number of videos on sdcard
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#videos-39)
   */
  val videos = Status(StatusId.VIDEOS, marshaller, ::toInt8)

  /**
   * OTA
   *
   * The current status of Over The Air (OTA) update
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-41)
   */
  val ota = Status(StatusId.OTA, marshaller, ::toInt8)

  /**
   * Pending FW Update Cancel
   *
   * Is there a pending request to cancel a firmware update download?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pending-fw-update-cancel-42)
   */
  val pendingFwUpdateCancel = Status(StatusId.PENDING_FW_UPDATE_CANCEL, marshaller, ::toBoolean)

  /**
   * Locate
   *
   * Is locate camera feature active?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#locate-45)
   */
  val locate = Status(StatusId.LOCATE, marshaller, ::toBoolean)

  /**
   * Timelapse Interval Countdown
   *
   * The current timelapse interval countdown value (e.g. 5...4...3...2...1...)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-interval-countdown-49)
   */
  val timelapseIntervalCountdown =
      Status(StatusId.TIMELAPSE_INTERVAL_COUNTDOWN, marshaller, ::toInt8)

  /**
   * SD Card Remaining
   *
   * Remaining space on the sdcard in Kilobytes
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-remaining-54)
   */
  val sdCardRemaining = Status(StatusId.SD_CARD_REMAINING, marshaller, ::toInt8)

  /**
   * Preview Stream Available
   *
   * Is preview stream supported in current recording/mode/secondary-stream?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-available-55)
   */
  val previewStreamAvailable = Status(StatusId.PREVIEW_STREAM_AVAILABLE, marshaller, ::toBoolean)

  /**
   * Wifi Bars
   *
   * WiFi signal strength in bars
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-bars-56)
   */
  val wifiBars = Status(StatusId.WIFI_BARS, marshaller, ::toInt8)

  /**
   * Active Hilights
   *
   * The number of hilights in currently-encoding video (value is set to 0 when encoding stops)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#active-hilights-58)
   */
  val activeHilights = Status(StatusId.ACTIVE_HILIGHTS, marshaller, ::toInt8)

  /**
   * Time Since Last Hilight
   *
   * Time since boot (milliseconds) of most recent hilight in encoding video (set to 0 when encoding
   * stops)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-since-last-hilight-59)
   */
  val timeSinceLastHilight = Status(StatusId.TIME_SINCE_LAST_HILIGHT, marshaller, ::toInt8)

  /**
   * Minimum Status Poll Period
   *
   * The minimum time between camera status updates (milliseconds). Best practice is to not poll for
   * status more often than this
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#minimum-status-poll-period-60)
   */
  val minimumStatusPollPeriod = Status(StatusId.MINIMUM_STATUS_POLL_PERIOD, marshaller, ::toInt8)

  /**
   * Liveview Exposure Select Mode
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-exposure-select-mode-65)
   */
  val liveviewExposureSelectMode =
      Status(StatusId.LIVEVIEW_EXPOSURE_SELECT_MODE, marshaller, ::toInt8)

  /**
   * Liveview Y
   *
   * Liveview Exposure Select: y-coordinate (percent)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-y-66)
   */
  val liveviewY = Status(StatusId.LIVEVIEW_Y, marshaller, ::toInt8)

  /**
   * Liveview X
   *
   * Liveview Exposure Select: y-coordinate (percent)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-x-67)
   */
  val liveviewX = Status(StatusId.LIVEVIEW_X, marshaller, ::toInt8)

  /**
   * GPS Lock
   *
   * Does the camera currently have a GPS lock?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#gps-lock-68)
   */
  val gpsLock = Status(StatusId.GPS_LOCK, marshaller, ::toBoolean)

  /**
   * AP Mode
   *
   * Is AP mode enabled?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ap-mode-69)
   */
  val apMode = Status(StatusId.AP_MODE, marshaller, ::toBoolean)

  /**
   * Internal Battery Percentage
   *
   * Internal battery level as percentage
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-percentage-70)
   */
  val internalBatteryPercentage = Status(StatusId.INTERNAL_BATTERY_PERCENTAGE, marshaller, ::toInt8)

  /**
   * Microphone Accessory
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#microphone-accessory-74)
   */
  val microphoneAccessory = Status(StatusId.MICROPHONE_ACCESSORY, marshaller, ::toInt8)

  /**
   * Zoom Level
   *
   * Digital Zoom level as percentage
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-level-75)
   */
  val zoomLevel = Status(StatusId.ZOOM_LEVEL, marshaller, ::toInt8)

  /**
   * Wireless Band
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-band-76)
   */
  val wirelessBand = Status(StatusId.WIRELESS_BAND, marshaller, ::toInt8)

  /**
   * Zoom Available
   *
   * Is Digital Zoom feature available?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-available-77)
   */
  val zoomAvailable = Status(StatusId.ZOOM_AVAILABLE, marshaller, ::toBoolean)

  /**
   * Mobile Friendly
   *
   * Are current video settings mobile friendly? (related to video compression and frame rate)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#mobile-friendly-78)
   */
  val mobileFriendly = Status(StatusId.MOBILE_FRIENDLY, marshaller, ::toBoolean)

  /**
   * FTU
   *
   * Is the camera currently in First Time Use (FTU) UI flow?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ftu-79)
   */
  val ftu = Status(StatusId.FTU, marshaller, ::toBoolean)

  /**
   * 5GHZ Available
   *
   * Is 5GHz wireless band available?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#5ghz-available-81)
   */
  val nUM5GhzAvailable = Status(StatusId.NUM_5GHZ_AVAILABLE, marshaller, ::toBoolean)

  /**
   * Ready
   *
   * Is the system fully booted and ready to accept commands?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ready-82)
   */
  val ready = Status(StatusId.READY, marshaller, ::toBoolean)

  /**
   * OTA Charged
   *
   * Is the internal battery charged sufficiently to start Over The Air (OTA) update?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-charged-83)
   */
  val otaCharged = Status(StatusId.OTA_CHARGED, marshaller, ::toBoolean)

  /**
   * Cold
   *
   * Is the camera getting too cold to continue recording?
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#cold-85)
   */
  val cold = Status(StatusId.COLD, marshaller, ::toBoolean)

  /**
   * Rotation
   *
   * Rotational orientation of the camera
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#rotation-86)
   */
  val rotation = Status(StatusId.ROTATION, marshaller, ::toInt8)

  /**
   * Zoom while Encoding
   *
   * Is this camera model capable of zooming while encoding?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-while-encoding-88)
   */
  val zoomWhileEncoding = Status(StatusId.ZOOM_WHILE_ENCODING, marshaller, ::toBoolean)

  /**
   * Flatmode
   *
   * Current Flatmode ID
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#flatmode-89)
   */
  val flatmode = Status(StatusId.FLATMODE, marshaller, ::toInt8)

  /**
   * Video Preset
   *
   * Current Video Preset (ID)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-preset-93)
   */
  val videoPreset = Status(StatusId.VIDEO_PRESET, marshaller, ::toInt8)

  /**
   * Photo Preset
   *
   * Current Photo Preset (ID)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-preset-94)
   */
  val photoPreset = Status(StatusId.PHOTO_PRESET, marshaller, ::toInt8)

  /**
   * Timelapse Preset
   *
   * Current Time Lapse Preset (ID)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-preset-95)
   */
  val timelapsePreset = Status(StatusId.TIMELAPSE_PRESET, marshaller, ::toInt8)

  /**
   * Preset Group
   *
   * Current Preset Group (ID) (corresponds to ui_mode_groups in settings.json)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-group-96)
   */
  val presetGroup = Status(StatusId.PRESET_GROUP, marshaller, ::toInt8)

  /**
   * Preset
   *
   * Current Preset (ID)
   *
   * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-97)
   */
  val preset = Status(StatusId.PRESET, marshaller, ::toInt8)

  /**
   * Preset Modified
   *
   * The value of this status is set to zero when the client sends a Get Preset Status message to
   * the camera.
   *
   * The value of this status is set to a non-zero value when:
   * - Preset settings submenu is exited in the camera UI (whether any settings were changed or not)
   * - A new preset is created
   * - A preset is deleted
   * - Preset ordering is changed within a preset group
   * - A preset is reset to factory defaults
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-modified-98)
   */
  val presetModified = Status(StatusId.PRESET_MODIFIED, marshaller, ::toInt8)

  /**
   * Remaining Live Bursts
   *
   * The number of Live Bursts can be captured with current settings before sdcard is full
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-live-bursts-99)
   */
  val remainingLiveBursts = Status(StatusId.REMAINING_LIVE_BURSTS, marshaller, ::toInt8)

  /**
   * Live Bursts
   *
   * Total number of Live Bursts on sdcard
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#live-bursts-100)
   */
  val liveBursts = Status(StatusId.LIVE_BURSTS, marshaller, ::toInt8)

  /**
   * Capture Delay Active
   *
   * Is Capture Delay currently active (i.e. counting down)?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#capture-delay-active-101)
   */
  val captureDelayActive = Status(StatusId.CAPTURE_DELAY_ACTIVE, marshaller, ::toBoolean)

  /**
   * Media Mod State
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#media-mod-state-102)
   */
  val mediaModState = Status(StatusId.MEDIA_MOD_STATE, marshaller, ::toInt8)

  /**
   * Time Warp Speed
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-warp-speed-103)
   */
  val timeWarpSpeed = Status(StatusId.TIME_WARP_SPEED, marshaller, ::toInt8)

  /**
   * Linux Core
   *
   * Is the system's Linux core active?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#linux-core-104)
   */
  val linuxCore = Status(StatusId.LINUX_CORE, marshaller, ::toBoolean)

  /**
   * Lens Type
   *
   * Camera lens type (reflects changes to lens settings such as 162, 189, 194, ...)
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lens-type-105)
   */
  val lensType = Status(StatusId.LENS_TYPE, marshaller, ::toInt8)

  /**
   * Hindsight
   *
   * Is Video Hindsight Capture Active?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#hindsight-106)
   */
  val hindsight = Status(StatusId.HINDSIGHT, marshaller, ::toBoolean)

  /**
   * Scheduled Capture Preset ID
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-preset-id-107)
   */
  val scheduledCapturePresetId = Status(StatusId.SCHEDULED_CAPTURE_PRESET_ID, marshaller, ::toInt8)

  /**
   * Scheduled Capture
   *
   * Is Scheduled Capture set?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-108)
   */
  val scheduledCapture = Status(StatusId.SCHEDULED_CAPTURE, marshaller, ::toBoolean)

  /**
   * Display Mod Status
   *
   * Note that this is a bitmasked value.
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#display-mod-status-110)
   */
  val displayModStatus = Status(StatusId.DISPLAY_MOD_STATUS, marshaller, ::toInt8)

  /**
   * SD Card Write Speed Error
   *
   * Is there an SD Card minimum write speed error?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-write-speed-error-111)
   */
  val sdCardWriteSpeedError = Status(StatusId.SD_CARD_WRITE_SPEED_ERROR, marshaller, ::toBoolean)

  /**
   * SD Card Errors
   *
   * Number of sdcard write speed errors since device booted
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-errors-112)
   */
  val sdCardErrors = Status(StatusId.SD_CARD_ERRORS, marshaller, ::toInt8)

  /**
   * Turbo Transfer
   *
   * Is Turbo Transfer active?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#turbo-transfer-113)
   */
  val turboTransfer = Status(StatusId.TURBO_TRANSFER, marshaller, ::toBoolean)

  /**
   * Camera Control ID
   *
   * Camera control status ID
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-control-id-114)
   */
  val cameraControlId = Status(StatusId.CAMERA_CONTROL_ID, marshaller, ::toInt8)

  /**
   * USB Connected
   *
   * Is the camera connected to a PC via USB?
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-connected-115)
   */
  val usbConnected = Status(StatusId.USB_CONNECTED, marshaller, ::toBoolean)

  /**
   * USB Controlled
   *
   * Camera control over USB state
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-controlled-116)
   */
  val usbControlled = Status(StatusId.USB_CONTROLLED, marshaller, ::toInt8)

  /**
   * SD Card Capacity
   *
   * Total SD card capacity in Kilobytes
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-capacity-117)
   */
  val sdCardCapacity = Status(StatusId.SD_CARD_CAPACITY, marshaller, ::toInt8)

  /**
   * Photo Interval Capture Count
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-interval-capture-count-118)
   */
  val photoIntervalCaptureCount =
      Status(StatusId.PHOTO_INTERVAL_CAPTURE_COUNT, marshaller, ::toInt8)

  /**
   * Camera Name
   *
   * Custom camera name set by the user
   *
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-name-122)
   */
  val cameraName = Status(StatusId.CAMERA_NAME, marshaller, ::toString)
}
