package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.communicator.CommunicationType
import entity.operation.CohnState
import entity.queries.Resolution
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class Busy(val text: String)

class CameraViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk,
) : BaseConnectedViewModel(appPreferences, wsdk, "CameraChooserViewModel") {
    private var _cohnState = MutableStateFlow(CohnState.Unprovisioned)
    val cohnState = _cohnState.asStateFlow()

    private var _isBusy = MutableStateFlow<Busy?>(null)
    val isBusy = _isBusy.asStateFlow()

    private var _isBleConnected = MutableStateFlow(false)
    val isBleConnected = _isBleConnected.asStateFlow()

    private var _isHttpConnected = MutableStateFlow(false)
    val isHttpConnected = _isHttpConnected.asStateFlow()

    private var shutter = false

    override fun onStart() {
        if (CommunicationType.BLE in gopro.communicators) {
            _isBleConnected.update { true }
        }
        if (CommunicationType.HTTP in gopro.communicators) {
            _isHttpConnected.update { true }
        }
        viewModelScope.launch {
            gopro.disconnects.collect { disconnect ->
                when (disconnect) {
                    CommunicationType.BLE -> {
                        _isBleConnected.update { false }
                    }

                    CommunicationType.HTTP -> {
                        _isHttpConnected.update { false }
                    }
                }
            }
        }
    }

    // TODO need to catch disconnects

    // Initial wifi connection needs to be done here because it relies on BLE.
    fun connectWifi() {
        viewModelScope.launch {
            _isBusy.update { Busy("Connecting Wifi...") }
            // TODO need to make this a callback from the GoPro for all connection types
            gopro.features.connectWifi.connect().onSuccess { _isHttpConnected.update { true } }
            _isBusy.update { null }

        }
    }

    fun toggleShutter() {
        viewModelScope.launch {
            gopro.commands.setShutter(shutter)
            shutter = !shutter
        }
    }

    fun sleep() = viewModelScope.launch { gopro.commands.sleep() }
}