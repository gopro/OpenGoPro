package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.queries.Resolution
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class SettingsUiState(val name: String) {
    data object Idle : SettingsUiState("idle")
    data object Scanning : SettingsUiState("scanning")
    data class WaitingConnect(val ssids: List<String>) : SettingsUiState("waiting to connect")
    data class Connecting(val ssid: String) : SettingsUiState("connecting to $ssid")
    data class Connected(val ssid: String) : SettingsUiState("connected to $ssid")
}

class SettingsViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk,
) : BaseConnectedViewModel(appPreferences, wsdk, "AccessPointViewModel") {
    private var _state = MutableStateFlow<SettingsUiState>(SettingsUiState.Idle)
    val state = _state.asStateFlow()

    private var _resolution = MutableStateFlow(Resolution.RES_1080)
    val resolution = _resolution.asStateFlow()

    fun registerResolutionValueUpdates() {
        viewModelScope.launch {
            gopro.settings.resolution.registerValueUpdate().onSuccess { flow ->
                flow.collect { resolutionUpdate ->
                    logger.d("ViewModel updating resolution to $resolutionUpdate")
                    _resolution.update { resolutionUpdate }
                }
            }
        }
    }
}