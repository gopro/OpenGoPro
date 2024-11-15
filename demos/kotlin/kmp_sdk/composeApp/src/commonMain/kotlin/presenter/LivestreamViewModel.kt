package presenter

import Wsdk
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import entity.operation.AccessPointState
import entity.operation.LivestreamConfigurationRequest
import entity.operation.LivestreamState
import entity.operation.LivestreamStatus
import gopro.GoPro
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class LivestreamUiState(val name: String) {
    data object ApNotConnected : LivestreamUiState("Not connected to Access Point")
    data object Ready : LivestreamUiState("Connected to AP. Ready for Livestream Config")
    data class Configuring(val url: String) :
        LivestreamUiState("Livestream config in progress to $url")

    data class Streaming(val status: LivestreamStatus) :
        LivestreamUiState("Streaming, status: ${status.status}\n error:${status.error}")
}

class LivestreamViewModel(
    private val appPreferences: IAppPreferences,
    private val wsdk: Wsdk
) : ViewModel() {
    private val logger = Logger.withTag("LivestreamViewModel")

    private lateinit var gopro: GoPro

    private var _state = MutableStateFlow<LivestreamUiState>(LivestreamUiState.ApNotConnected)
    val state = _state.asStateFlow()

    // TODO take in URL and other params
    private val rtmpUrl = "rtmp://192.168.50.66:1935/live/test"
    val hlsUrl = "http://192.168.50.66:8080"

    fun startStream() =
        viewModelScope.launch {
            _state.update { LivestreamUiState.Configuring(rtmpUrl) }
            logger.i("Configuring livestream.")
            gopro.commands.startLivestream(LivestreamConfigurationRequest(url = rtmpUrl))
            gopro.commands.getLivestreamStatuses().getOrThrow().collect { livestreamState ->
                _state.update { LivestreamUiState.Streaming(livestreamState) }
                if (livestreamState.status == LivestreamState.READY) {
                    logger.i("Livestream has been configured. Starting streaming.")
                    gopro.commands.setShutter(true)
                }
            }
        }

    fun start() {
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = wsdk.getGoPro(it)
            } ?: throw Exception("No connected device found.")

            if (gopro.accessPointState.value is AccessPointState.Connected) {
                _state.update { LivestreamUiState.Ready }
            } else {
                _state.update { LivestreamUiState.ApNotConnected }
            }
        }
    }

    fun stop() {

    }
}