package presenter

import Wsdk
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import entity.operation.CohnState
import entity.queries.Resolution
import gopro.GoPro
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

private val logger = Logger.withTag("CameraChooserViewModel")

sealed class CameraUiState {
    data object Idle : CameraUiState()
    data object Initializing : CameraUiState()
    data object Ready : CameraUiState()
}

class CameraViewModel(
    private val appPreferences: IAppPreferences,
    private val wsdk: Wsdk,
) : ViewModel() {
    private lateinit var gopro: GoPro
    private var _state = MutableStateFlow<CameraUiState>(CameraUiState.Idle)
    val state = _state.asStateFlow()

    private var _resolution = MutableStateFlow(Resolution.RES_1080)
    val resolution = _resolution.asStateFlow()

    private var _cohnState = MutableStateFlow(CohnState.Unprovisioned)
    val cohnState = _cohnState.asStateFlow()

    // Initial wifi connection needs to be done here because it relies on BLE.
    fun connectWifi() {
        viewModelScope.launch {
            gopro.features.connectWifi.connect()
        }
    }

    fun start() {
        viewModelScope.launch {
            _state.update { CameraUiState.Initializing }
            appPreferences.getConnectedDevice()?.let {
                gopro = wsdk.getGoPro(it)
            } ?: throw Exception("No connected device found.")
            _state.update { CameraUiState.Ready }
        }
    }

    fun stop() {
        // TODO disconnect?
    }

    fun registerResolutionValueUpdates() {
        viewModelScope.launch {
            gopro.settings.resolution.registerValueUpdate().onSuccess { (currentValue, flow) ->
                _resolution.update { currentValue }
                flow.collect { resolutionUpdate ->
                    logger.d("ViewModel updating resolution to $resolutionUpdate")
                    _resolution.update { resolutionUpdate }
                }
            }
            gopro.cohnState.collect {
                _cohnState.update { it }
            }
        }
    }

    private val _shutter = MutableStateFlow(false)

    fun toggleShutter() {
        viewModelScope.launch {
            gopro.commands.setShutter(_shutter.value)
            _shutter.update { !_shutter.value }
        }
    }
}