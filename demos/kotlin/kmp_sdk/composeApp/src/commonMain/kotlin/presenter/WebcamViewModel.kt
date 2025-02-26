/* WebcamViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.WebcamError
import com.gopro.open_gopro.operations.WebcamProtocol
import com.gopro.open_gopro.operations.WebcamStatus
import data.IAppPreferences
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class WebcamUiState(val message: String) {
  data class Error(val error: String) : WebcamUiState("Error: $error")

  data object Ready : WebcamUiState("Ready to start Webcam")

  data class Starting(val status: WebcamStatus) : WebcamUiState("Webcam Starting: ${status.name}")

  data class Streaming(val error: WebcamError) : WebcamUiState("Webcam Streaming: ${error.name}")
}

class WebcamViewModel(appPreferences: IAppPreferences, sdk: OgpSdk) :
    BaseConnectedViewModel(appPreferences, sdk, "WebcamViewModel") {
  private var _state = MutableStateFlow<WebcamUiState>(WebcamUiState.Error("not yet initialized"))
  val state = _state.asStateFlow()

  private var statusPollJob: Job? = null

  fun streamUrl(protocol: WebcamProtocol): String =
      gopro.ipAddress?.let { cameraIp ->
        if (protocol == WebcamProtocol.RTSP) "rtsp://$cameraIp:554/live" else "udp://@:8554"
      } ?: throw Exception("Camera has no IP address")

  fun startStream(protocol: WebcamProtocol) =
      viewModelScope.launch {
        statusPollJob =
            viewModelScope.launch {
              while (true) {
                gopro.commands.getWebcamState().getOrThrow().let { state ->
                  when (state.status) {
                    WebcamStatus.HIGH_POWER_PREVIEW -> {
                      _state.update { WebcamUiState.Streaming(state.error) }
                    }

                    else -> _state.update { WebcamUiState.Starting(state.status) }
                  }
                }
                delay(2000)
              }
            }
        logger.i("Starting webcam stream with $protocol")
        gopro.commands.startWebcam(protocol = protocol)
      }

  fun stopStream() =
      viewModelScope.launch {
        gopro.commands.stopWebcam()
        statusPollJob?.cancel()
        _state.update { WebcamUiState.Ready }
      }

  override fun onStart() {
    if (gopro.isHttpAvailable) {
      _state.update { WebcamUiState.Ready }
    } else {
      _state.update { WebcamUiState.Error("HTTP not available.") }
    }
  }

  override fun stop() {
    if (_state.value is WebcamUiState.Streaming) {
      statusPollJob?.cancel()
      stopStream()
    }
    super.stop()
  }
}
