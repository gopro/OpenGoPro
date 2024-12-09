package gopro

/************************************************************************************************************
 *
 *
 * WARNING!!! This file is auto-generated. Do not modify it manually
 *
 *
 */

import domain.api.IOperationMarshaller
import entity.queries.*
import domain.queries.Status
import util.extensions.decodeToString
import util.extensions.toBoolean

@OptIn(ExperimentalUnsignedTypes::class)
private fun toBoolean(data: UByteArray): Boolean = data.last().toBoolean()

@OptIn(ExperimentalUnsignedTypes::class)
private fun toInt8(data: UByteArray): Int = data.last().toInt()

@OptIn(ExperimentalUnsignedTypes::class)
private fun toString(data: UByteArray): String = data.decodeToString()

/**
 * Container for all per-status-ID wrappers
 *
 * Note! This is a very small subset of the supported statuses. TODO these need to be automatically
 * generated.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html)
 *
 * @param marshaller
 */
@OptIn(ExperimentalUnsignedTypes::class)
class StatusesContainer internal constructor(marshaller: IOperationMarshaller) {

    /**
     * Battery Present
     *
     * Is the system's internal battery present?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Battery-Present-1)
     *
     * @property value
     */
    val batteryPresent = Status(StatusId.BATTERY_PRESENT, marshaller,::toBoolean)

    /**
     * Internal Battery Bars
     *
     * Rough approximation of internal battery level in bars (or charging)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Internal-Battery-Bars-2)
     *
     * @property value
     */
    val internalBatteryBars = Status(StatusId.INTERNAL_BATTERY_BARS, marshaller,::toInt8)

    /**
     * External Battery
     *
     * Is an external battery connected?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#External-Battery-3)
     *
     * @property value
     */
    val externalBattery = Status(StatusId.EXTERNAL_BATTERY, marshaller,::toBoolean)

    /**
     * External Battery Percentage
     *
     * External battery power level as percentage
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#External-Battery-Percentage-4)
     *
     * @property value
     */
    val externalBatteryPercentage = Status(StatusId.EXTERNAL_BATTERY_PERCENTAGE, marshaller,::toInt8)

    /**
     * Overheating
     *
     * Is the system currently overheating?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Overheating-6)
     *
     * @property value
     */
    val overheating = Status(StatusId.OVERHEATING, marshaller,::toBoolean)

    /**
     * Busy
     *
     * Is the camera busy?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Busy-8)
     *
     * @property value
     */
    val busy = Status(StatusId.BUSY, marshaller,::toBoolean)

    /**
     * Quick Capture
     *
     * Is Quick Capture feature enabled?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Quick-Capture-9)
     *
     * @property value
     */
    val quickCapture = Status(StatusId.QUICK_CAPTURE, marshaller,::toBoolean)

    /**
     * Encoding
     *
     * Is the system currently encoding?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Encoding-10)
     *
     * @property value
     */
    val encoding = Status(StatusId.ENCODING, marshaller,::toBoolean)

    /**
     * LCD Lock
     *
     * Is LCD lock active?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#LCD-Lock-11)
     *
     * @property value
     */
    val lcdLock = Status(StatusId.LCD_LOCK, marshaller,::toBoolean)

    /**
     * Video Encoding Duration
     *
     * When encoding video, this is the duration (seconds) of the video so far; 0 otherwise
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Video-Encoding-Duration-13)
     *
     * @property value
     */
    val videoEncodingDuration = Status(StatusId.VIDEO_ENCODING_DURATION, marshaller,::toInt8)

    /**
     * Broadcast Duration
     *
     * When broadcasting (Live Stream), this is the broadcast duration (seconds) so far; 0 otherwise
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Broadcast-Duration-14)
     *
     * @property value
     */
    val broadcastDuration = Status(StatusId.BROADCAST_DURATION, marshaller,::toInt8)

    /**
     * Wireless Connections Enabled
     *
     * Are Wireless Connections enabled?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Wireless-Connections-Enabled-17)
     *
     * @property value
     */
    val wirelessConnectionsEnabled = Status(StatusId.WIRELESS_CONNECTIONS_ENABLED, marshaller,::toBoolean)

    /**
     * Pairing State
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Pairing-State-19)
     *
     * @property value
     */
    val pairingState = Status(StatusId.PAIRING_STATE, marshaller,::toInt8)

    /**
     * Last Pairing Type
     *
     * The last type of pairing in which the camera was engaged
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Last-Pairing-Type-20)
     *
     * @property value
     */
    val lastPairingType = Status(StatusId.LAST_PAIRING_TYPE, marshaller,::toInt8)

    /**
     * Last Pairing Success
     *
     * Time since boot (milliseconds) of last successful pairing complete action
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Last-Pairing-Success-21)
     *
     * @property value
     */
    val lastPairingSuccess = Status(StatusId.LAST_PAIRING_SUCCESS, marshaller,::toInt8)

    /**
     * Wifi Scan State
     *
     * State of current scan for WiFi Access Points
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Wifi-Scan-State-22)
     *
     * @property value
     */
    val wifiScanState = Status(StatusId.WIFI_SCAN_STATE, marshaller,::toInt8)

    /**
     * Last Wifi Scan Success
     *
     * Time since boot (milliseconds) that the WiFi Access Point scan completed
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Last-Wifi-Scan-Success-23)
     *
     * @property value
     */
    val lastWifiScanSuccess = Status(StatusId.LAST_WIFI_SCAN_SUCCESS, marshaller,::toInt8)

    /**
     * Wifi Provisioning State
     *
     * WiFi AP provisioning state
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Wifi-Provisioning-State-24)
     *
     * @property value
     */
    val wifiProvisioningState = Status(StatusId.WIFI_PROVISIONING_STATE, marshaller,::toInt8)

    /**
     * Remote Version
     *
     * Wireless remote control version
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remote-Version-26)
     *
     * @property value
     */
    val remoteVersion = Status(StatusId.REMOTE_VERSION, marshaller,::toInt8)

    /**
     * Remote Connected
     *
     * Is a wireless remote control connected?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remote-Connected-27)
     *
     * @property value
     */
    val remoteConnected = Status(StatusId.REMOTE_CONNECTED, marshaller,::toBoolean)

    /**
     * Pairing State (Legacy)
     *
     * Wireless Pairing State. Each bit contains state information (see WirelessPairingStateFlags)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Pairing-State-(Legacy)-28)
     *
     * @property value
     */
    val pairingState_Legacy_ = Status(StatusId.PAIRING_STATE_LEGACY_, marshaller,::toInt8)

    /**
     * AP SSID
     *
     * SSID of the AP the camera is currently connected to when the camera is connected as a STA. When read via BLE,
     * value is big-endian byte-encoded int32.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#AP-SSID-29)
     *
     * @property value
     */
    val apSsid = Status(StatusId.AP_SSID, marshaller,::toString
    )

    /**
     * WiFi SSID
     *
     * The camera's WiFi SSID. On BLE connection, value is big-endian byte-encoded int32
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#WiFi-SSID-30)
     *
     * @property value
     */
    val wifiSsid = Status(StatusId.WIFI_SSID, marshaller,::toString
    )

    /**
     * Connected Devices
     *
     * The number of wireless devices connected to the camera
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Connected-Devices-31)
     *
     * @property value
     */
    val connectedDevices = Status(StatusId.CONNECTED_DEVICES, marshaller,::toInt8)

    /**
     * Preview Stream
     *
     * Is Preview Stream enabled?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Preview-Stream-32)
     *
     * @property value
     */
    val previewStream = Status(StatusId.PREVIEW_STREAM, marshaller,::toBoolean)

    /**
     * Primary Storage
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Primary-Storage-33)
     *
     * @property value
     */
    val primaryStorage = Status(StatusId.PRIMARY_STORAGE, marshaller,::toInt8)

    /**
     * Remaining Photos
     *
     * How many photos can be taken with current settings before sdcard is full.
     *
     * Alternatively, this is:
     *
     * - the remaining timelapse capability if Setting 128 is set to Timelapse Photo
     * - the remaining nightlapse capability if Setting 128 is set to Nightlapse Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remaining-Photos-34)
     *
     * @property value
     */
    val remainingPhotos = Status(StatusId.REMAINING_PHOTOS, marshaller,::toInt8)

    /**
     * Remaining Video Time
     *
     * How many seconds of video can be captured with current settings before sdcard is full
     *
     * Alternatively, this is:
     *
     * - the remaining timelapse capability if Setting 128 is set to Timelapse Video
     * - the remaining nightlapse capability if Setting 128 is set to Nightlapse Video
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remaining-Video-Time-35)
     *
     * @property value
     */
    val remainingVideoTime = Status(StatusId.REMAINING_VIDEO_TIME, marshaller,::toInt8)

    /**
     * Group Photos
     *
     * Total number of group photos on sdcard
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Group-Photos-36)
     *
     * @property value
     */
    val groupPhotos = Status(StatusId.GROUP_PHOTOS, marshaller,::toInt8)

    /**
     * Chaptered Videos
     *
     * Total number of chaptered videos on sdcard
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Chaptered-Videos-37)
     *
     * @property value
     */
    val chapteredVideos = Status(StatusId.CHAPTERED_VIDEOS, marshaller,::toInt8)

    /**
     * Photos
     *
     * Total number of photos on sdcard
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Photos-38)
     *
     * @property value
     */
    val photos = Status(StatusId.PHOTOS, marshaller,::toInt8)

    /**
     * Videos
     *
     * Total number of videos on sdcard
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Videos-39)
     *
     * @property value
     */
    val videos = Status(StatusId.VIDEOS, marshaller,::toInt8)

    /**
     * OTA
     *
     * The current status of Over The Air (OTA) update
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#OTA-41)
     *
     * @property value
     */
    val ota = Status(StatusId.OTA, marshaller,::toInt8)

    /**
     * Pending FW Update Cancel
     *
     * Is there a pending request to cancel a firmware update download?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Pending-FW-Update-Cancel-42)
     *
     * @property value
     */
    val pendingFwUpdateCancel = Status(StatusId.PENDING_FW_UPDATE_CANCEL, marshaller,::toBoolean)

    /**
     * Locate
     *
     * Is locate camera feature active?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Locate-45)
     *
     * @property value
     */
    val locate = Status(StatusId.LOCATE, marshaller,::toBoolean)

    /**
     * Timelapse Interval Countdown
     *
     * The current timelapse interval countdown value (e.g. 5...4...3...2...1...)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Timelapse-Interval-Countdown-49)
     *
     * @property value
     */
    val timelapseIntervalCountdown = Status(StatusId.TIMELAPSE_INTERVAL_COUNTDOWN, marshaller,::toInt8)

    /**
     * SD Card Remaining
     *
     * Remaining space on the sdcard in Kilobytes
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#SD-Card-Remaining-54)
     *
     * @property value
     */
    val sdCardRemaining = Status(StatusId.SD_CARD_REMAINING, marshaller,::toInt8)

    /**
     * Preview Stream Available
     *
     * Is preview stream supported in current recording/mode/secondary-stream?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Preview-Stream-Available-55)
     *
     * @property value
     */
    val previewStreamAvailable = Status(StatusId.PREVIEW_STREAM_AVAILABLE, marshaller,::toBoolean)

    /**
     * Wifi Bars
     *
     * WiFi signal strength in bars
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Wifi-Bars-56)
     *
     * @property value
     */
    val wifiBars = Status(StatusId.WIFI_BARS, marshaller,::toInt8)

    /**
     * Active Hilights
     *
     * The number of hilights in currently-encoding video (value is set to 0 when encoding stops)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Active-Hilights-58)
     *
     * @property value
     */
    val activeHilights = Status(StatusId.ACTIVE_HILIGHTS, marshaller,::toInt8)

    /**
     * Time Since Last Hilight
     *
     * Time since boot (milliseconds) of most recent hilight in encoding video (set to 0 when encoding stops)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Time-Since-Last-Hilight-59)
     *
     * @property value
     */
    val timeSinceLastHilight = Status(StatusId.TIME_SINCE_LAST_HILIGHT, marshaller,::toInt8)

    /**
     * Minimum Status Poll Period
     *
     * The minimum time between camera status updates (milliseconds). Best practice is to not poll for status more
     * often than this
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Minimum-Status-Poll-Period-60)
     *
     * @property value
     */
    val minimumStatusPollPeriod = Status(StatusId.MINIMUM_STATUS_POLL_PERIOD, marshaller,::toInt8)

    /**
     * Analytics
     *
     * The current state of camera analytics
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Analytics-61)
     *
     * @property value
     */
    val analytics = Status(StatusId.ANALYTICS, marshaller,::toInt8)

    /**
     * Analytics Size
     *
     * The size (units??) of the analytics file
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Analytics-Size-62)
     *
     * @property value
     */
    val analyticsSize = Status(StatusId.ANALYTICS_SIZE, marshaller,::toInt8)

    /**
     * In Contextual Menu
     *
     * Is the camera currently in a contextual menu (e.g. Preferences)?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#In-Contextual-Menu-63)
     *
     * @property value
     */
    val inContextualMenu = Status(StatusId.IN_CONTEXTUAL_MENU, marshaller,::toBoolean)

    /**
     * Remaining Timelapse
     *
     * How many seconds of Time Lapse Video can be captured with current settings before sdcard is full
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remaining-Timelapse-64)
     *
     * @property value
     */
    val remainingTimelapse = Status(StatusId.REMAINING_TIMELAPSE, marshaller,::toInt8)

    /**
     * Liveview Exposure Select Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Liveview-Exposure-Select-Mode-65)
     *
     * @property value
     */
    val liveviewExposureSelectMode = Status(StatusId.LIVEVIEW_EXPOSURE_SELECT_MODE, marshaller,::toInt8)

    /**
     * Liveview Y
     *
     * Liveview Exposure Select: y-coordinate (percent)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Liveview-Y-66)
     *
     * @property value
     */
    val liveviewY = Status(StatusId.LIVEVIEW_Y, marshaller,::toInt8)

    /**
     * Liveview X
     *
     * Liveview Exposure Select: y-coordinate (percent)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Liveview-X-67)
     *
     * @property value
     */
    val liveviewX = Status(StatusId.LIVEVIEW_X, marshaller,::toInt8)

    /**
     * GPS Lock
     *
     * Does the camera currently have a GPS lock?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#GPS-Lock-68)
     *
     * @property value
     */
    val gpsLock = Status(StatusId.GPS_LOCK, marshaller,::toBoolean)

    /**
     * AP Mode
     *
     * Is AP mode enabled?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#AP-Mode-69)
     *
     * @property value
     */
    val apMode = Status(StatusId.AP_MODE, marshaller,::toBoolean)

    /**
     * Internal Battery Percentage
     *
     * Internal battery level as percentage
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Internal-Battery-Percentage-70)
     *
     * @property value
     */
    val internalBatteryPercentage = Status(StatusId.INTERNAL_BATTERY_PERCENTAGE, marshaller,::toInt8)

    /**
     * Microphone Accessory
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Microphone-Accessory-74)
     *
     * @property value
     */
    val microphoneAccessory = Status(StatusId.MICROPHONE_ACCESSORY, marshaller,::toInt8)

    /**
     * Zoom Level
     *
     * Digital Zoom level as percentage
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Zoom-Level-75)
     *
     * @property value
     */
    val zoomLevel = Status(StatusId.ZOOM_LEVEL, marshaller,::toInt8)

    /**
     * Wireless Band
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Wireless-Band-76)
     *
     * @property value
     */
    val wirelessBand = Status(StatusId.WIRELESS_BAND, marshaller,::toInt8)

    /**
     * Zoom Available
     *
     * Is Digital Zoom feature available?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Zoom-Available-77)
     *
     * @property value
     */
    val zoomAvailable = Status(StatusId.ZOOM_AVAILABLE, marshaller,::toBoolean)

    /**
     * Mobile Friendly
     *
     * Are current video settings mobile friendly? (related to video compression and frame rate)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Mobile-Friendly-78)
     *
     * @property value
     */
    val mobileFriendly = Status(StatusId.MOBILE_FRIENDLY, marshaller,::toBoolean)

    /**
     * FTU
     *
     * Is the camera currently in First Time Use (FTU) UI flow?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#FTU-79)
     *
     * @property value
     */
    val ftu = Status(StatusId.FTU, marshaller,::toBoolean)

    /**
     * 5GHZ Available
     *
     * Is 5GHz wireless band available?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#5GHZ-Available-81)
     *
     * @property value
     */
    val nUM5GhzAvailable = Status(StatusId.NUM_5GHZ_AVAILABLE, marshaller,::toBoolean)

    /**
     * Ready
     *
     * Is the system fully booted and ready to accept commands?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Ready-82)
     *
     * @property value
     */
    val ready = Status(StatusId.READY, marshaller,::toBoolean)

    /**
     * OTA Charged
     *
     * Is the internal battery charged sufficiently to start Over The Air (OTA) update?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#OTA-Charged-83)
     *
     * @property value
     */
    val otaCharged = Status(StatusId.OTA_CHARGED, marshaller,::toBoolean)

    /**
     * Cold
     *
     * Is the camera getting too cold to continue recording?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Cold-85)
     *
     * @property value
     */
    val cold = Status(StatusId.COLD, marshaller,::toBoolean)

    /**
     * Rotation
     *
     * Rotational orientation of the camera
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Rotation-86)
     *
     * @property value
     */
    val rotation = Status(StatusId.ROTATION, marshaller,::toInt8)

    /**
     * Zoom while Encoding
     *
     * Is this camera model capable of zooming while encoding?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Zoom-while-Encoding-88)
     *
     * @property value
     */
    val zoomWhileEncoding = Status(StatusId.ZOOM_WHILE_ENCODING, marshaller,::toBoolean)

    /**
     * Flatmode
     *
     * Current Flatmode ID
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Flatmode-89)
     *
     * @property value
     */
    val flatmode = Status(StatusId.FLATMODE, marshaller,::toInt8)

    /**
     * Default Protune
     *
     * Are current flatmode's Protune settings factory default?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Default-Protune-90)
     *
     * @property value
     */
    val defaultProtune = Status(StatusId.DEFAULT_PROTUNE, marshaller,::toBoolean)

    /**
     * Logs Ready
     *
     * Are system logs ready to be downloaded?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Logs-Ready-91)
     *
     * @property value
     */
    val logsReady = Status(StatusId.LOGS_READY, marshaller,::toBoolean)

    /**
     * Video Preset
     *
     * Current Video Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Video-Preset-93)
     *
     * @property value
     */
    val videoPreset = Status(StatusId.VIDEO_PRESET, marshaller,::toInt8)

    /**
     * Photo Preset
     *
     * Current Photo Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Photo-Preset-94)
     *
     * @property value
     */
    val photoPreset = Status(StatusId.PHOTO_PRESET, marshaller,::toInt8)

    /**
     * Timelapse Preset
     *
     * Current Time Lapse Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Timelapse-Preset-95)
     *
     * @property value
     */
    val timelapsePreset = Status(StatusId.TIMELAPSE_PRESET, marshaller,::toInt8)

    /**
     * Preset Group
     *
     * Current Preset Group (ID) (corresponds to ui_mode_groups in settings.json)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Preset-Group-96)
     *
     * @property value
     */
    val presetGroup = Status(StatusId.PRESET_GROUP, marshaller,::toInt8)

    /**
     * Preset
     *
     * Current Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Preset-97)
     *
     * @property value
     */
    val preset = Status(StatusId.PRESET, marshaller,::toInt8)

    /**
     * Preset Modified
     *
     * Preset Modified Status, which contains an event ID and a Preset (Group) ID
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Preset-Modified-98)
     *
     * @property value
     */
    val presetModified = Status(StatusId.PRESET_MODIFIED, marshaller,::toInt8)

    /**
     * Remaining Live Bursts
     *
     * The number of Live Bursts can be captured with current settings before sdcard is full
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Remaining-Live-Bursts-99)
     *
     * @property value
     */
    val remainingLiveBursts = Status(StatusId.REMAINING_LIVE_BURSTS, marshaller,::toInt8)

    /**
     * Live Bursts
     *
     * Total number of Live Bursts on sdcard
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Live-Bursts-100)
     *
     * @property value
     */
    val liveBursts = Status(StatusId.LIVE_BURSTS, marshaller,::toInt8)

    /**
     * Capture Delay Active
     *
     * Is Capture Delay currently active (i.e. counting down)?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Capture-Delay-Active-101)
     *
     * @property value
     */
    val captureDelayActive = Status(StatusId.CAPTURE_DELAY_ACTIVE, marshaller,::toBoolean)

    /**
     * Media Mod State
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Media-Mod-State-102)
     *
     * @property value
     */
    val mediaModState = Status(StatusId.MEDIA_MOD_STATE, marshaller,::toInt8)

    /**
     * Time Warp Speed
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Time-Warp-Speed-103)
     *
     * @property value
     */
    val timeWarpSpeed = Status(StatusId.TIME_WARP_SPEED, marshaller,::toInt8)

    /**
     * Linux Core
     *
     * Is the system's Linux core active?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Linux-Core-104)
     *
     * @property value
     */
    val linuxCore = Status(StatusId.LINUX_CORE, marshaller,::toBoolean)

    /**
     * Lens Type
     *
     * Camera lens type (reflects changes to lens settings such as 162, 189, 194, ...)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Lens-Type-105)
     *
     * @property value
     */
    val lensType = Status(StatusId.LENS_TYPE, marshaller,::toInt8)

    /**
     * Hindsight
     *
     * Is Video Hindsight Capture Active?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Hindsight-106)
     *
     * @property value
     */
    val hindsight = Status(StatusId.HINDSIGHT, marshaller,::toBoolean)

    /**
     * Scheduled Capture Preset ID
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Scheduled-Capture-Preset-ID-107)
     *
     * @property value
     */
    val scheduledCapturePresetId = Status(StatusId.SCHEDULED_CAPTURE_PRESET_ID, marshaller,::toInt8)

    /**
     * Scheduled Capture
     *
     * Is Scheduled Capture set?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Scheduled-Capture-108)
     *
     * @property value
     */
    val scheduledCapture = Status(StatusId.SCHEDULED_CAPTURE, marshaller,::toBoolean)

    /**
     * Custom Preset
     *
     * Is the camera in the process of creating a custom preset?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Custom-Preset-109)
     *
     * @property value
     */
    val customPreset = Status(StatusId.CUSTOM_PRESET, marshaller,::toBoolean)

    /**
     * Display Mod Status
     *
     * Note that this is a bitmasked value.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Display-Mod-Status-110)
     *
     * @property value
     */
    val displayModStatus = Status(StatusId.DISPLAY_MOD_STATUS, marshaller,::toInt8)

    /**
     * SD Card Write Speed Error
     *
     * Is there an SD Card minimum write speed error?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#SD-Card-Write-Speed-Error-111)
     *
     * @property value
     */
    val sdCardWriteSpeedError = Status(StatusId.SD_CARD_WRITE_SPEED_ERROR, marshaller,::toBoolean)

    /**
     * SD Card Errors
     *
     * Number of sdcard write speed errors since device booted
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#SD-Card-Errors-112)
     *
     * @property value
     */
    val sdCardErrors = Status(StatusId.SD_CARD_ERRORS, marshaller,::toInt8)

    /**
     * Turbo Transfer
     *
     * Is Turbo Transfer active?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Turbo-Transfer-113)
     *
     * @property value
     */
    val turboTransfer = Status(StatusId.TURBO_TRANSFER, marshaller,::toBoolean)

    /**
     * Camera Control ID
     *
     * Camera control status ID
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Camera-Control-ID-114)
     *
     * @property value
     */
    val cameraControlId = Status(StatusId.CAMERA_CONTROL_ID, marshaller,::toInt8)

    /**
     * USB Connected
     *
     * Is the camera connected to a PC via USB?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#USB-Connected-115)
     *
     * @property value
     */
    val usbConnected = Status(StatusId.USB_CONNECTED, marshaller,::toBoolean)

    /**
     * USB Controlled
     *
     * Camera control over USB state
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#USB-Controlled-116)
     *
     * @property value
     */
    val usbControlled = Status(StatusId.USB_CONTROLLED, marshaller,::toInt8)

    /**
     * SD Card Capacity
     *
     * Total SD card capacity in Kilobytes
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#SD-Card-Capacity-117)
     *
     * @property value
     */
    val sdCardCapacity = Status(StatusId.SD_CARD_CAPACITY, marshaller,::toInt8)

    /**
     * Photo Interval Capture Count
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Photo-Interval-Capture-Count-118)
     *
     * @property value
     */
    val photoIntervalCaptureCount = Status(StatusId.PHOTO_INTERVAL_CAPTURE_COUNT, marshaller,::toInt8)

    /**
     * Camera Lens Mod
     *
     * Camera lens mod (reflects changes to lens settings such as 162, 189, 194, ...)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Camera-Lens-Mod-119)
     *
     * @property value
     */
    val cameraLensMod = Status(StatusId.CAMERA_LENS_MOD, marshaller,::toInt8)

    /**
     * POV Preset
     *
     * Current POV Group Active Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#POV-Preset-120)
     *
     * @property value
     */
    val povPreset = Status(StatusId.POV_PRESET, marshaller,::toInt8)

    /**
     * Selfie Preset
     *
     * Current Selfie Group Active Preset (ID)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#Selfie-Preset-121)
     *
     * @property value
     */
    val selfiePreset = Status(StatusId.SELFIE_PRESET, marshaller,::toInt8);
}