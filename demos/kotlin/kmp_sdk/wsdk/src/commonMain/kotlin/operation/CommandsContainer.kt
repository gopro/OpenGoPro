package operation

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

// TODO strategy needs to be cleaned up. We need a different enum because it doesn't make sense
// to pick HTTP vs HTTPS. Also there should be a "first available" option.

class CommandsContainer(private val marshaller: IOperationMarshaller) {
    suspend fun setShutter(value: Boolean) =
        marshaller.marshal(SetShutter(value)) {
            isFastpass { operation, _ -> operation.shutter }
        }

    suspend fun readWifiSsid() = marshaller.marshal(ReadWifiSsid())

    suspend fun readWifiPassword() = marshaller.marshal(ReadWifiPassword())

    suspend fun setApMode(enable: Boolean) = marshaller.marshal(SetApMode(enable))

    suspend fun getMediaList() =
        marshaller.marshal(MediaGetList()) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getMediaMetadata(file: MediaId) =
        marshaller.marshal(MediaGetMetadata(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun downloadMedia(file: MediaId) =
        marshaller.marshal(MediaDownload(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getScreenNail(file: MediaId) =
        marshaller.marshal(MediaGetScreennail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun getThumbNail(file: MediaId) =
        marshaller.marshal(MediaGetThumbnail(file)) { useCommunicator { _, _ -> CommunicationType.HTTP } }

    suspend fun sendKeepAlive() =
        marshaller.marshal(KeepAlive()) { useCommunicator { _, _ -> CommunicationType.BLE } }

    suspend fun getHardwareInfo() = marshaller.marshal(GetHardwareInfo())

    suspend fun setCameraControl(status: CameraControlStatus) =
        marshaller.marshal(SetCameraControl(status))

    suspend fun configureLivestream(request: LivestreamConfigurationRequest) =
        marshaller.marshal(LivestreamConfigure(request))

    suspend fun startPreviewStream() = marshaller.marshal(PreviewStreamStart()) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    suspend fun stopPreviewStream() = marshaller.marshal(PreviewStreamStop()) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    suspend fun startWebcam(
        resolution: WebcamResolution? = null,
        fov: WebcamFov? = null,
        port: Int? = null,
        protocol: WebcamProtocol? = null
    ) = marshaller.marshal(WebcamStart(resolution, fov, port, protocol)) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    suspend fun startLivestream(request: LivestreamConfigurationRequest) =
        marshaller.marshal(LivestreamConfigure(request))

    suspend fun getLivestreamState() = marshaller.marshal(LivestreamGetStatus())

    suspend fun stopWebcam() = marshaller.marshal(WebcamStop()) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    suspend fun getWebcamState() = marshaller.marshal(WebcamGetState()) {
        useCommunicator { _, _ -> CommunicationType.HTTP }
    }

    suspend fun setDateTime(
        datetime: LocalDateTime,
        utcOffset: UtcOffset,
        isDaylightSavings: Boolean
    ) = marshaller.marshal(DatetimeSet(datetime, utcOffset, isDaylightSavings))
}
