package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.operation.AccessPointState
import entity.operation.CohnState
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

class CohnViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk
) : BaseConnectedViewModel(appPreferences, wsdk, "CohnViewModel") {
    private var _state = MutableStateFlow<CohnUiState>(CohnUiState.Idle)
    val state = _state.asStateFlow()

    fun provision() {
        when (_state.value) {
            is CohnUiState.Idle ->
                viewModelScope.launch {
                    _state.update { CohnUiState.Provisioning }
                    gopro.features.cohn.provisionCohn().getOrThrow()
                    _state.update { CohnUiState.ProvisionedAndReady }
                }

            else -> logger.e("Can only provision COHN from Idle state.")
        }
    }

    override fun onStart() {
        when (gopro.cohnState.value) {
            is CohnState.Provisioned -> _state.update { CohnUiState.ProvisionedAndReady }
            else -> _state.update {
                if (gopro.accessPointState.value is AccessPointState.Connected) {
                    CohnUiState.Idle
                } else {
                    CohnUiState.ApNotConnected
                }
            }
        }
    }
}