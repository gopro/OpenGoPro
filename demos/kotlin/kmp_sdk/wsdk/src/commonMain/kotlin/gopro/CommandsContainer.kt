package gopro

import domain.api.IOperationMarshaller
import entity.communicator.CommunicationType
import entity.media.MediaId
import entity.operation.CameraControlStatus
import entity.operation.LivestreamConfigurationRequest
import entity.operation.WebcamFov
import entity.operation.WebcamProtocol
import entity.operation.WebcamResolution
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
import operation.commands.DatetimeSet
import operation.commands.GetHardwareInfo
import operation.commands.KeepAlive
import operation.commands.LivestreamConfigure
import operation.commands.LivestreamGetStatus
import operation.commands.MediaDownload
import operation.commands.MediaGetList
import operation.commands.MediaGetMetadata
import operation.commands.MediaGetScreennail
import operation.commands.MediaGetThumbnail
import operation.commands.PresetGetInfo
import operation.commands.PreviewStreamStart
import operation.commands.PreviewStreamStop
import operation.commands.ReadWifiPassword
import operation.commands.ReadWifiSsid
import operation.commands.SetApMode
import operation.commands.SetCameraControl
import operation.commands.SetShutter
import operation.commands.WebcamGetState
import operation.commands.WebcamStart
import operation.commands.WebcamStop

class CommandsContainer internal constructor(marshaller: IOperationMarshaller) :
    IOperationMarshaller by marshaller {
    /**
     * Enable / disable the shutter to start / stop encoding
     *
     * @param value true to enable, false to disable
     */
    suspend fun setShutter(value: Boolean) =
        marshal(SetShutter(value)) {
            isFastpass { operation, _ -> operation.shutter }
        }

    suspend fun readWifiSsid() =
        marshal(ReadWifiSsid())

    suspend fun readWifiPassword() =
        marshal(ReadWifiPassword())

    suspend fun setApMode(enable: Boolean) =
        marshal(SetApMode(enable))

    suspend fun getMediaList() =
        marshal(MediaGetList()) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getMediaMetadata(file: MediaId) =
        marshal(MediaGetMetadata(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun downloadMedia(file: MediaId) =
        marshal(MediaDownload(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getScreenNail(file: MediaId) =
        marshal(MediaGetScreennail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getThumbNail(file: MediaId) =
        marshal(MediaGetThumbnail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun sendKeepAlive() =
        marshal(KeepAlive()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun getHardwareInfo() =
        marshal(GetHardwareInfo())

    suspend fun setCameraControl(status: CameraControlStatus) =
        marshal(SetCameraControl(status))

    suspend fun configureLivestream(request: LivestreamConfigurationRequest) =
        marshal(LivestreamConfigure(request))

    suspend fun startPreviewStream() =
        marshal(PreviewStreamStart()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    suspend fun stopPreviewStream() =
        marshal(PreviewStreamStop()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    suspend fun startWebcam(
        resolution: WebcamResolution? = null,
        fov: WebcamFov? = null,
        port: Int? = null,
        protocol: WebcamProtocol? = null
    ) =
        marshal(WebcamStart(resolution, fov, port, protocol)) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    suspend fun startLivestream(request: LivestreamConfigurationRequest) =
        marshal(LivestreamConfigure(request))

    suspend fun getLivestreamState() =
        marshal(LivestreamGetStatus())

    suspend fun stopWebcam() =
        marshal(WebcamStop()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    suspend fun getWebcamState() =
        marshal(WebcamGetState()) {
            useCommunicator { _, _ -> CommunicationType.HTTP }
        }

    suspend fun scanAccessPoint() =
        marshal(AccessPointScan())

    suspend fun getAccessPointScanResults(scanId: Int, totalEntries: Int) =
        marshal(AccessPointGetScanResults(scanId, totalEntries))

    suspend fun connectAccessPoint(ssid: String) =
        marshal(ConnectProvisionedAccessPoint(ssid))

    suspend fun connectAccessPoint(ssid: String, password: String) =
        marshal(ConnectNewAccessPoint(ssid, password))

    suspend fun getPresetInfo() =
        marshal(PresetGetInfo())

    suspend fun getCohnStatus() =
        marshal(CohnGetStatus())


    suspend fun getCohnCertificate() =
        marshal(CohnGetCert())

    suspend fun clearCohnCertificate() =
        marshal(CohnClearCert())

    suspend fun createCohnCertificate(override: Boolean) =
        marshal(CohnCreateCert(override))

    suspend fun setDateTime(
        datetime: LocalDateTime,
        utcOffset: UtcOffset,
        isDaylightSavings: Boolean
    ) =
        marshal(DatetimeSet(datetime, utcOffset, isDaylightSavings))
}
