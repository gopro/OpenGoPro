package gopro

import domain.api.IOperationMarshaller
import entity.communicator.CommunicationType
import entity.operation.CameraControlStatus
import entity.operation.GpDatetime
import entity.operation.HardwareInfo
import entity.operation.LivestreamConfigurationRequest
import entity.operation.LivestreamStatus
import entity.operation.MediaId
import entity.operation.MediaList
import entity.operation.MediaMetadata
import entity.operation.PresetGroupId
import entity.operation.PresetInfo
import entity.operation.WebcamFov
import entity.operation.WebcamProtocol
import entity.operation.WebcamResolution
import entity.operation.WebcamState
import kotlinx.coroutines.flow.Flow
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.UtcOffset
import operation.commands.AccessPointGetScanResults
import operation.commands.AccessPointScan
import operation.commands.CohnClearCert
import operation.commands.CohnCreateCert
import operation.commands.CohnGetCert
import operation.commands.CohnGetStatus
import operation.commands.ConnectNewAccessPoint
import operation.commands.ConnectProvisionedAccessPoint
import operation.commands.DatetimeGet
import operation.commands.DatetimeSet
import operation.commands.GetHardwareInfo
import operation.commands.HilightFile
import operation.commands.HilightMoment
import operation.commands.HilightRemove
import operation.commands.KeepAlive
import operation.commands.LivestreamConfigure
import operation.commands.LivestreamGetStatus
import operation.commands.MediaDeleteAll
import operation.commands.MediaDeleteGrouped
import operation.commands.MediaDeleteSingle
import operation.commands.MediaDownload
import operation.commands.MediaGetLastCaptured
import operation.commands.MediaGetList
import operation.commands.MediaGetMetadata
import operation.commands.MediaGetScreennail
import operation.commands.MediaGetThumbnail
import operation.commands.PresetGetInfo
import operation.commands.PresetLoad
import operation.commands.PresetLoadGroup
import operation.commands.PreviewStreamStart
import operation.commands.PreviewStreamStop
import operation.commands.ReadWifiPassword
import operation.commands.ReadWifiSsid
import operation.commands.SetApMode
import operation.commands.SetCameraControl
import operation.commands.SetDigitalZoom
import operation.commands.SetShutter
import operation.commands.WebcamGetState
import operation.commands.WebcamStart
import operation.commands.WebcamStop

/**
 * Wrapper to access operations exposed as methods.
 *
 * @property marshaller operation marshaller to marshal wrapped operations.
 */
class CommandsContainer internal constructor(private val marshaller: IOperationMarshaller) {
    /**
     * Enable / disable the shutter to start / stop encoding
     *
     * @param value true to enable, false to disable
     */
    suspend fun setShutter(value: Boolean): Result<Unit> =
        marshaller.marshal(SetShutter(value)) {
            // It's always fastpass
            isFastpass { _, _ -> true }
            // We can't complete the command until encoding has completed
            waitForEncodingStop { operation, _ -> !operation.shutter }
        }

    /**
     * Get the Media List
     *
     * @see [Open GoPro spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_MEDIA_LIST)
     *
     * @return Media List
     */
    suspend fun getMediaList(): Result<MediaList> =
        marshaller.marshal(MediaGetList()) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    /**
     * Get Media Metadata for a single media file
     *
     * @see [Open GoPro spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_MEDIA_INFO)
     *
     * @param file File to query
     *
     * @return media metadata for queried file
     */
    suspend fun getMediaMetadata(file: MediaId): Result<MediaMetadata> =
        marshaller.marshal(MediaGetMetadata(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }


    /**
     * Download a media file
     *
     * @param file file to download
     * @return binary media file
     */
    suspend fun downloadMedia(file: MediaId): Result<ByteArray> =
        marshaller.marshal(MediaDownload(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }


    /**
     * Download a screennail for a given media file
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_MEDIA_SCREENNAIL)
     *
     * @param file screennail to download
     * @return binary screennail image
     */
    suspend fun getScreenNail(file: MediaId): Result<ByteArray> =
        marshaller.marshal(MediaGetScreennail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    /**
     * Download a thumbnail for a given media file
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_MEDIA_THUMBNAIL)
     *
     * @param file thumbnail to download
     * @return binary thumbnail image
     */
    suspend fun getThumbNail(file: MediaId): Result<ByteArray> =
        marshaller.marshal(MediaGetThumbnail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    /**
     * Get hardware information of the connected camera
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Query/operation/OGP_CAMERA_INFO)
     * @return hardware information
     */
    suspend fun getHardwareInfo(): Result<HardwareInfo> =
        marshaller.marshal(GetHardwareInfo())

    /**
     * Configure and start livestreaming
     *
     * @param request livestream configuration parameters
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#set-livestream-mode)
     */
    suspend fun startLivestream(request: LivestreamConfigurationRequest) =
        marshaller.marshal(LivestreamConfigure(request))

    /**
     * Get continuous livestream statuses
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#get-livestream-status)
     * @return flow of livestream statuses
     */
    suspend fun getLivestreamStatuses(): Result<Flow<LivestreamStatus>> =
        marshaller.marshal(LivestreamGetStatus())

    /**
     * Start the preview stream
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Preview-Stream)
     */
    suspend fun startPreviewStream() =
        marshaller.marshal(PreviewStreamStart()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Stop the preview stream
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Preview-Stream/operation/OGP_PREVIEW_STREAM_STOP)
     */
    suspend fun stopPreviewStream() =
        marshaller.marshal(PreviewStreamStop()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Start wireless webcam streaming
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Webcam)
     *
     * @param resolution desired resolution
     * @param fov desired field of view
     * @param port desired port. If null, defaults to 8554 by the camera
     * @param protocol desired protocol. If null, defaults to TS by the camera
     */
    suspend fun startWebcam(
        resolution: WebcamResolution? = null,
        fov: WebcamFov? = null,
        port: Int? = null,
        protocol: WebcamProtocol? = null
    ) =
        marshaller.marshal(WebcamStart(resolution, fov, port, protocol)) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Stop the wireless webcam
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Webcam/operation/GPCAMERA_WEBCAM_STOP_OGP)
     */
    suspend fun stopWebcam() =
        marshaller.marshal(WebcamStop()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Get the current webcam state
     *
     * Note! There is way to register for asynchronous updates so this must be polled if desired.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Webcam/operation/GPCAMERA_WEBCAM_STATUS_OGP)
     *
     * @return the current webcam state
     */
    suspend fun getWebcamState(): Result<WebcamState> =
        marshaller.marshal(WebcamGetState()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Get available presets and related preset information
     *
     * @see [Open GoPro](https://gopro.github.io/OpenGoPro/http#tag/Presets/operation/OGP_PRESETS_GET)
     */
    suspend fun getPresetInfo(): Result<Flow<PresetInfo>> =
        marshaller.marshal(PresetGetInfo())

    /**
     * Set the camera's date and time.
     *
     * Note! The camera certificate's used by [gopro.features.CohnFeature] require that this time is correct.
     * It is not recommended to set this manually.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/control.html#set-local-date-time)
     *
     * @param datetime date and time
     * @param utcOffset UTC offset in minutes
     * @param isDaylightSavings true if daylight savings time. false otherwise
     */
    suspend fun setDateTime(
        datetime: LocalDateTime,
        utcOffset: UtcOffset,
        isDaylightSavings: Boolean
    ) =
        marshaller.marshal(DatetimeSet(datetime, utcOffset, isDaylightSavings))

    /**
     * Get the camera's current date and time
     *
     * @see [OpenGoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-date-time)
     *
     * @return GoPro DateTime including UTC offset and daylight savings time
     */
    suspend fun getDateTime(): Result<GpDatetime> = marshaller.marshal(DatetimeGet())

    /**
     * Add a hilight / tag to an existing photo or media file
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Hilights/operation/OGP_ADD_HILIGHT)
     *
     * @param file file to add hilight to
     * @param offsetMs millisecond offset into video file to add hilight. Not applicable for photos.
     */
    suspend fun hilightFile(file: MediaId, offsetMs: Int? = null) =
        marshaller.marshal(HilightFile(file, offsetMs)) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Add hilight at current time while recording video
     *
     * This can only be used during recording.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Hilights/operation/OGP_TAG_MOMENT)
     */
    suspend fun hilightMoment() = marshaller.marshal(HilightMoment())

    /**
     * Remove an existing hilight from a photo or video file
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Hilights/operation/OGP_REMOVE_HILIGHT)
     *
     * @param file file to remove hilight from
     * @param offsetMs millisecond offset into video file to remove hilight. Not applicable for photos.
     */
    suspend fun hilightRemove(file: MediaId, offsetMs: Int?) =
        marshaller.marshal(HilightRemove(file, offsetMs)) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    /**
     * Delete all media files on the SD card
     *
     * @see [Open GoPro spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/GPCAMERA_DELETE_ALL_FILES_ID)
     */
    suspend fun deleteAllMedia() = marshaller.marshal(MediaDeleteAll()) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    /**
     * Delete an entire group of media files such as in a burst, timelapse, or chaptered video.
     *
     * This API should not be used to delete single files. Instead use [deleteSingleMedia]
     *
     * @see [Open GoPro spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/GPCAMERA_DELETE_FILE_GROUP)
     *
     * @param group grouped media to delete
     */
    suspend fun deleteGroupedMedia(group: MediaId) = marshaller.marshal(MediaDeleteGrouped(group)) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    /**
     * Delete a single media file
     *
     * When operating on a file that is part of a group, only the individual file will be deleted.
     * To delete the entire group, use [deleteGroupedMedia]
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_DELETE_SINGLE_FILE)
     *
     * @param file file to delete
     */
    suspend fun deleteSingleMedia(file: MediaId) = marshaller.marshal(MediaDeleteSingle(file)) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    /**
     * Get the last captured media file ID
     *
     * This will return the complete path of the last captured media. Depending on the type of media
     * captured, it will return:
     *   - single photo / video: The single media path
     *   - any grouped media: The path to the first captured media in the group
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Media/operation/OGP_GET_LAST_MEDIA)
     *
     * @return last captured media file ID
     */
    suspend fun getLastCapturedMediaFileId(): Result<MediaId> =
        marshaller.marshal(MediaGetLastCaptured())

    /**
     * Load a preset by ID
     *
     * A preset can only be loaded if it is currently available where available preset IDs can be
     * found with [getPresetInfo]
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/http#tag/Presets/operation/OGP_PRESET_LOAD)
     *
     * @param presetId preset ID to load
     */
    suspend fun loadPreset(presetId: Int) = marshaller.marshal(PresetLoad(presetId))

    /**
     * Load a preset group by ID
     *
     * @see [Preset Groups](https://gopro.github.io/OpenGoPro/http#tag/Presets/Preset-Groups)
     *
     * @param group preset Group ID to load
     */
    suspend fun loadPresetGroup(group: PresetGroupId) = marshaller.marshal(PresetLoadGroup(group))

    /**
     * Set the camera's digital zoom
     *
     * @see [Preset Group](https://gopro.github.io/OpenGoPro/http#tag/Control/operation/OGP_DIGITAL_ZOOM_SET)
     *
     * @param zoom desired zoom percentage from 1-100
     */
    suspend fun setDigitalZoom(zoom: Int) = marshaller.marshal(SetDigitalZoom(zoom))

    /***********************************************************************************************
     * Internal. These are abstracted through a feature or set via [GoPro]
     */

    internal suspend fun sendKeepAlive() =
        marshaller.marshal(KeepAlive()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    internal suspend fun scanAccessPoint() =
        marshaller.marshal(AccessPointScan())

    internal suspend fun getAccessPointScanResults(scanId: Int, totalEntries: Int) =
        marshaller.marshal(AccessPointGetScanResults(scanId, totalEntries))

    internal suspend fun connectAccessPoint(ssid: String) =
        marshaller.marshal(ConnectProvisionedAccessPoint(ssid))

    internal suspend fun connectAccessPoint(ssid: String, password: String) =
        marshaller.marshal(ConnectNewAccessPoint(ssid, password))

    internal suspend fun getCohnStatus() =
        marshaller.marshal(CohnGetStatus())

    internal suspend fun getCohnCertificate() =
        marshaller.marshal(CohnGetCert())

    internal suspend fun clearCohnCertificate() =
        marshaller.marshal(CohnClearCert())

    internal suspend fun createCohnCertificate(override: Boolean) =
        marshaller.marshal(CohnCreateCert(override))

    /**
     * Read the camera's Access Point SSID
     *
     * This is the SSID that is used to connect to the camera when the camera is operating as
     * an Access Point.
     *
     * @see [Access Point Mode](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#access-point-mode-ap)
     *
     * @return SSID string
     */
    suspend fun readWifiSsid(): Result<String> =
        marshaller.marshal(ReadWifiSsid())

    /**
     * Read the camera's Access Point password
     *
     * This is the password that is used to connect to the camera when the camera is operating as
     * an Access Point.
     *
     * @see [Access Point Mode](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#access-point-mode-ap)
     *
     * @return password string
     */
    suspend fun readWifiPassword(): Result<String> =
        marshaller.marshal(ReadWifiPassword())

    /**
     * Set camera Access Point on / off
     *
     * This enables / disables connections to the camera where the camers is operating as an
     * Access Point
     *
     * @see [Access Point Mode](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#access-point-mode-ap)
     *
     * @param enable true to enable. false to disable
     */
    suspend fun setApMode(enable: Boolean) =
        marshaller.marshal(SetApMode(enable))

    // TODO where / should we use this?
    internal suspend fun setCameraControl(status: CameraControlStatus) =
        marshaller.marshal(SetCameraControl(status))
}
