/* AccessPointViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.AccessPointState
import data.IAppPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class ApUiState(val name: String) {
  data object Idle : ApUiState("idle")

  data object Scanning : ApUiState("scanning")

  data class WaitingConnect(val ssids: List<String>) : ApUiState("waiting to connect")

  data class Connecting(val ssid: String) : ApUiState("connecting to $ssid")

  data class Connected(val ssid: String) : ApUiState("connected to $ssid")
}

class AccessPointViewModel(
    appPreferences: IAppPreferences,
    sdk: OgpSdk,
) : BaseConnectedViewModel(appPreferences, sdk, "AccessPointViewModel") {
  private var _state = MutableStateFlow<ApUiState>(ApUiState.Idle)
  val state = _state.asStateFlow()

  private var _errorMessage = MutableStateFlow<String?>(null)
  val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()

  private fun setErrorMessage(message: String) {
    logger.e(message)
    _errorMessage.update { message }
  }

  private fun setState(newState: ApUiState) {
    logger.d("Setting state to: ${newState.name}")
    _state.update { newState }
  }

  fun scanForSsids() {
    if (_state.value == ApUiState.Idle) {
      viewModelScope.launch {
        setState(ApUiState.Scanning)
        gopro.features.accessPoint
            .scanForAccessPoints()
            .getOrThrow()
            .map { it.ssid }
            .let { ssids -> setState(ApUiState.WaitingConnect(ssids)) }
      }
    } else {
      setErrorMessage("Can only scan from idle state")
    }
  }

  fun connectToSsid(ssid: String) {
    if (_state.value is ApUiState.WaitingConnect) {
      viewModelScope.launch {
        setState(ApUiState.Connecting(ssid))
        gopro.features.accessPoint
            .connectAccessPoint(ssid)
            .onSuccess { setState(ApUiState.Connected(ssid)) }
            .onFailure { setState(ApUiState.Idle) }
      }
    } else {
      setErrorMessage("Can only connect after scanning.")
    }
  }

  fun connectToSsid(ssid: String, password: String) {
    if (_state.value is ApUiState.WaitingConnect) {
      viewModelScope.launch {
        setState(ApUiState.Connecting(ssid))
        gopro.features.accessPoint
            .connectAccessPoint(ssid, password)
            .onSuccess { setState(ApUiState.Connected(ssid)) }
            .onFailure { setState(ApUiState.Idle) }
      }
    } else {
      setErrorMessage("Can only connect after scanning.")
    }
  }

  fun disconnect() {
    if (_state.value is ApUiState.Connected) {
      viewModelScope.launch {
        gopro.features.accessPoint
            .disconnectAccessPoint()
            .onSuccess { setState(ApUiState.Idle) }
            .onFailure { setErrorMessage("Failed to disconnect from access point") }
      }
    } else {
      setErrorMessage("Can only disconnect when connected.")
    }
  }

  override fun onStart() {
    when (val featureState = gopro.accessPointState.value) {
      AccessPointState.Disconnected -> ApUiState.Idle
      is AccessPointState.InProgress -> ApUiState.Connecting(featureState.ssid)
      is AccessPointState.Connected -> ApUiState.Connected(featureState.ssid)
    }.let { setState(it) }
  }
}
