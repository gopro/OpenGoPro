package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.operation.WebcamError
import entity.operation.WebcamProtocol
import entity.operation.WebcamStatus
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class WebcamViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk
) : BaseConnectedViewModel(appPreferences, wsdk, "WebcamViewModel") {
    private var _status = MutableStateFlow(WebcamStatus.OFF)
    val status = _status.asStateFlow()
    private var _error = MutableStateFlow(WebcamError.NONE)
    val error = _error.asStateFlow()
    private var _protocol = MutableStateFlow(WebcamProtocol.RTSP)
    private val protocol = _protocol.asStateFlow()

    private var statusPollJob: Job? = null

    val streamUrl: String
        get() = gopro.ipAddress?.let { cameraIp ->
            if (protocol.value == WebcamProtocol.RTSP) "rtsp://$cameraIp:554/live" else "udp://@:8554"
        } ?: throw Exception("Camera has no IP address")


    fun startStream(protocol: WebcamProtocol) =
        viewModelScope.launch {
            _protocol.update { protocol }
            logger.i("Starting webcam stream with $protocol")
            gopro.commands.startWebcam(protocol = protocol)
        }

    fun stopStream() =
        viewModelScope.launch {
            gopro.commands.stopWebcam()
        }

    override fun onStart() {
        statusPollJob = viewModelScope.launch {
            while (true) {
                gopro.commands.getWebcamState().getOrThrow().let { state ->
                    _status.update { state.status }
                    _error.update { state.error }
                }
                delay(2000)
            }
        }
    }

    override fun stop() {
        statusPollJob?.cancel()
        super.stop()
    }
}