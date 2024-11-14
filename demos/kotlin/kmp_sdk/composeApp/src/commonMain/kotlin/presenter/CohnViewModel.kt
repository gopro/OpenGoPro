package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import domain.gopro.IGoProFactory
import entity.operation.AccessPointState
import entity.operation.CohnState
import gopro.GoPro
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

private val logger = Logger.withTag("CohnViewModel")

sealed class CohnUiState(val name: String) {
    data object ApNotConnected : CohnUiState("Not connected to Access Point")
    data object Idle : CohnUiState("idle")
    data object Provisioning : CohnUiState("provisioning")
    data object ProvisionedAndReady : CohnUiState("ready for communication via COHN")
}

class CohnViewModel(
    private val appPreferences: IAppPreferences,
    private val goProFactory: IGoProFactory,
) : ViewModel() {
    private lateinit var gopro: GoPro

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

    fun start() {
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = goProFactory.getGoPro(it)
            } ?: throw Exception("No connected device found.")

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

    fun stop() {

    }
}