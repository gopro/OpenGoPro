package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.operation.AccessPointState
import entity.operation.LivestreamConfigurationRequest
import entity.operation.LivestreamState
import entity.operation.LivestreamStatus
import kotlinx.coroutines.delay
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
    appPreferences: IAppPreferences,
    wsdk: Wsdk
) : BaseConnectedViewModel(appPreferences, wsdk, "LivestreamViewModel") {
    private var _state = MutableStateFlow<LivestreamUiState>(LivestreamUiState.ApNotConnected)
    val state = _state.asStateFlow()

    fun startStream(url: String) =
        viewModelScope.launch {
            _state.update { LivestreamUiState.Configuring(url) }
            logger.i("Configuring livestream.")
            gopro.commands.startLivestream(LivestreamConfigurationRequest(url = url))
            gopro.commands.getLivestreamStatuses().getOrThrow().collect { livestreamState ->
                logger.d("Livestream state: $livestreamState")
                if (livestreamState.status == LivestreamState.READY) {
                    logger.i("Livestream has been configured. Starting streaming.")
                    gopro.commands.setShutter(true)
                    // TODO what's going on here? It's probably just an issue with my test media server
                    delay(5000)
                    _state.update { LivestreamUiState.Streaming(livestreamState) }
                }
            }
        }

    fun stopStream() = viewModelScope.launch {
        gopro.commands.setShutter(false)
        _state.update { LivestreamUiState.Ready }
    }

    override fun onStart() {
        if (gopro.accessPointState.value is AccessPointState.Connected) {
            _state.update { LivestreamUiState.Ready }
        } else {
            _state.update { LivestreamUiState.ApNotConnected }
        }
    }
}