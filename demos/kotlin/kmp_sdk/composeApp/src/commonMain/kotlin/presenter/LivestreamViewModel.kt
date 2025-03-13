/* LivestreamViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.LivestreamConfigurationRequest
import com.gopro.open_gopro.operations.LivestreamState
import com.gopro.open_gopro.operations.LivestreamStatus
import data.IAppPreferences
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

class LivestreamViewModel(appPreferences: IAppPreferences, sdk: OgpSdk) :
    BaseConnectedViewModel(appPreferences, sdk, "LivestreamViewModel") {
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

  fun stopStream() =
      viewModelScope.launch {
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
