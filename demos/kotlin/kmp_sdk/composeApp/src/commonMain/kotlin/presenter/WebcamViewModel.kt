package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import entity.operation.WebcamError
import entity.operation.WebcamProtocol
import entity.operation.WebcamStatus
import gopro.GoPro
import gopro.IGoProFactory
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

private val logger = Logger.withTag("WebcamViewModel")

class WebcamViewModel(
    private val appPreferences: IAppPreferences,
    private val goProFactory: IGoProFactory,
) : ViewModel() {
    private lateinit var gopro: GoPro

    private var _status = MutableStateFlow(WebcamStatus.OFF)
    val status = _status.asStateFlow()
    private var _error = MutableStateFlow(WebcamError.NONE)
    val error = _error.asStateFlow()
    private var _protocol = MutableStateFlow(WebcamProtocol.RTSP)
    private val protocol = _protocol.asStateFlow()

    private var statusPollJob: Job? = null

    // TODO we need access to the IP address.
    val streamUrl
        get() = if (protocol.value == WebcamProtocol.RTSP) "rtsp://192.168.50.209:554/live" else "udp://@:8554"


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

    fun start() {
        viewModelScope.launch {
            viewModelScope.launch {
                appPreferences.getConnectedDevice()?.let {
                    gopro = goProFactory.getGoPro(it)
                } ?: throw Exception("No connected device found.")
            }.join()

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
    }

    fun stop() {
        statusPollJob?.cancel()
    }
}