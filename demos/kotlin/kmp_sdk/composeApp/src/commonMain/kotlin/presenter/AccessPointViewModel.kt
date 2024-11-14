package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import entity.operation.AccessPointState
import gopro.GoPro
import gopro.IGoProFactory
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
    private val appPreferences: IAppPreferences,
    private val goProFactory: IGoProFactory,
) : ViewModel() {
    private val logger = Logger.withTag("AccessPointViewModel")

    private lateinit var gopro: GoPro

    private var _state = MutableStateFlow<ApUiState>(ApUiState.Idle)
    val state = _state.asStateFlow()

    fun scanForSsids() {
        if (_state.value == ApUiState.Idle) {
            viewModelScope.launch {
                _state.update { ApUiState.Scanning }
                gopro.features.accessPoint.scanForAccessPoints().getOrThrow().map { it.ssid }
                    .let { ssids ->
                        _state.update { ApUiState.WaitingConnect(ssids) }
                    }
            }
        } else {
            logger.w("Can only scan from idle state")
        }
    }

    private suspend fun processConnectNotifications(notifications: Flow<AccessPointState>) =
        _state.value.let { s ->
            if (s is ApUiState.Connecting) {
                notifications.collect { notification ->
                    logger.d("Received AP Connect notification: $notification")
                    when (notification) {
                        is AccessPointState.Connected -> _state.update { ApUiState.Connected(s.ssid) }
                        is AccessPointState.InProgress -> _state.update { ApUiState.Connecting(s.ssid) }
                        else -> _state.update { ApUiState.Idle }
                    }
                }
            } else {
                logger.w("Can not process connect notifications if not connecting")
            }
        }

    fun connectToSsid(ssid: String) {
        if (_state.value is ApUiState.WaitingConnect) {
            viewModelScope.launch {
                _state.update { ApUiState.Connecting(ssid) }
                processConnectNotifications(
                    gopro.features.accessPoint.connectAccessPoint(ssid).getOrThrow()
                )
            }
        } else {
            logger.w("Can only connect after scanning.")
        }
    }

    fun connectToSsid(ssid: String, password: String) {
        if (_state.value is ApUiState.WaitingConnect) {
            viewModelScope.launch {
                _state.update { ApUiState.Connecting(ssid) }
                processConnectNotifications(
                    gopro.features.accessPoint.connectAccessPoint(ssid, password).getOrThrow()
                )
            }
        } else {
            logger.w("Can only connect after scanning.")
        }
    }

    fun start() {
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = goProFactory.getGoPro(it)
            } ?: throw Exception("No connected device found.")
        }
    }

    fun stop() {

    }
}