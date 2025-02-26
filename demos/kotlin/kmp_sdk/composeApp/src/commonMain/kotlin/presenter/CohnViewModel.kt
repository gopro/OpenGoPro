/* CohnViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.CohnState
import data.IAppPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class CohnUiState(val name: String) {
  data object ApNotConnected : CohnUiState("Not connected to Access Point")

  data object Idle : CohnUiState("idle")

  data object Provisioning : CohnUiState("provisioning")

  data object ProvisionedAndReady : CohnUiState("ready for communication via COHN")
}

class CohnViewModel(appPreferences: IAppPreferences, sdk: OgpSdk) :
    BaseConnectedViewModel(appPreferences, sdk, "CohnViewModel") {
  private var _state = MutableStateFlow<CohnUiState>(CohnUiState.Idle)
  val state = _state.asStateFlow()

  fun provision() {
    when (_state.value) {
      is CohnUiState.Idle ->
          viewModelScope.launch {
            _state.update { CohnUiState.Provisioning }
            gopro.features.cohn.provision().getOrThrow()
            _state.update { CohnUiState.ProvisionedAndReady }
          }

      else -> logger.e("Can only provision COHN from Idle state.")
    }
  }

  fun enable() {
    viewModelScope.launch { gopro.features.cohn.enable() }
  }

  fun disable() {
    viewModelScope.launch { gopro.features.cohn.disable() }
  }

  fun unprovision() {
    viewModelScope.launch { gopro.features.cohn.unprovision() }
  }

  override fun onStart() {
    when (gopro.cohnState.value) {
      is CohnState.Provisioned -> _state.update { CohnUiState.ProvisionedAndReady }
      else ->
          _state.update {
            if (gopro.accessPointState.value is AccessPointState.Connected) {
              CohnUiState.Idle
            } else {
              CohnUiState.ApNotConnected
            }
          }
    }
  }
}
