/* AccessPointViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.AccessPointState
import data.IAppPreferences
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
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

    fun scanForSsids() {
        if (_state.value == ApUiState.Idle) {
            viewModelScope.launch {
                _state.update { ApUiState.Scanning }
                gopro.features.accessPoint
                    .scanForAccessPoints()
                    .getOrThrow()
                    .map { it.ssid }
                    .let { ssids -> _state.update { ApUiState.WaitingConnect(ssids) } }
            }
        } else {
            logger.w("Can only scan from idle state")
        }
    }

    fun connectToSsid(ssid: String) {
        if (_state.value is ApUiState.WaitingConnect) {
            viewModelScope.launch {
                _state.update { ApUiState.Connecting(ssid) }
                gopro.features.accessPoint.connectAccessPoint(ssid)
                    .onSuccess { _state.update { ApUiState.Connected(ssid) } }
                    .onFailure { _state.update { ApUiState.Idle } }
            }
        } else {
            logger.w("Can only connect after scanning.")
        }
    }

    fun connectToSsid(ssid: String, password: String) {
        if (_state.value is ApUiState.WaitingConnect) {
            viewModelScope.launch {
                _state.update { ApUiState.Connecting(ssid) }
                gopro.features.accessPoint.connectAccessPoint(ssid, password)
                    .onSuccess { _state.update { ApUiState.Connected(ssid) } }
                    .onFailure { _state.update { ApUiState.Idle } }
            }
        } else {
            logger.w("Can only connect after scanning.")
        }
    }

    fun disconnect() {
        if (_state.value is ApUiState.Connected) {
            viewModelScope.launch {
                gopro.features.accessPoint.disconnectAccessPoint()
                    .onSuccess { _state.update { ApUiState.Idle } }
                    .onFailure { logger.e("Failed to disconnect from access point") }
            }
        } else {
            logger.w("Can only disconnect when connected.")
        }
    }
}
