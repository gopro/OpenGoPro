package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import domain.connector.ICameraConnector
import domain.gopro.IGoProFactory
import entity.connector.ConnectionRequestContext
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.onCompletion
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

private val logger = Logger.withTag("CameraChooserViewModel")

enum class ScanNetworkType {
    BLE,
    WIFI,
    DNS
}

private fun scanNetworkToNetwork(scanNetworkType: ScanNetworkType): NetworkType =
    when (scanNetworkType) {
        ScanNetworkType.BLE -> NetworkType.BLE
        ScanNetworkType.WIFI -> NetworkType.WIFI_AP
        ScanNetworkType.DNS -> NetworkType.WIFI_WLAN
    }

sealed class CameraChooserUiState(val name: String) {
    data object Idle : CameraChooserUiState("Discover")
    data object Discovering : CameraChooserUiState("Cancel")
    data object Connecting : CameraChooserUiState("Connected!")
    data object Connected : CameraChooserUiState("Connecting...")
}

class CameraChooserViewModel(
    private val connector: ICameraConnector,
    private val appPreferences: IAppPreferences,
) : ViewModel() {
    private val found = hashMapOf<String, ScanResult>() // Used to prevent duplicates
    private val _devices = MutableStateFlow<List<ScanResult>>(listOf())
    val devices = _devices.asStateFlow()

    private var discoverJob: Job? = null
    private var _state = MutableStateFlow<CameraChooserUiState>(CameraChooserUiState.Idle)
    val state = _state.asStateFlow()


    fun discover(networks: Set<ScanNetworkType>) {
        if (_state.value == CameraChooserUiState.Idle) {
            discoverJob = viewModelScope.launch {
                // TODO fix network types here. It doesn't make sense.
                connector.discover(*networks.map(::scanNetworkToNetwork).toTypedArray())
                    .onStart {
                        _state.update { CameraChooserUiState.Discovering }
                    }
                    .onEach {
                        found[it.serialId] = it
                    }.onCompletion {
                        _devices.update { mutableListOf() }
                    }
                    .collect {
                        _devices.update { found.values.toList() }
                    }
            }
        } else {
            logger.w { "Already discovering" }
        }
    }

    fun cancelDiscovery() {
        if (_state.value == CameraChooserUiState.Discovering) {
            discoverJob?.cancel()
            // TODO Should we join? Where?
            discoverJob = null
            _state.update { CameraChooserUiState.Idle }
        } else {
            logger.w { "Can't cancel since not discovering." }
        }
    }


    fun connect(target: ScanResult) {
        if (_state.value != CameraChooserUiState.Discovering) {
            logger.w { "Can only connect from discovery state." }
            return
        }

        val requestContext: ConnectionRequestContext? = when (target) {
            // TODO this needs to be retrieved from DB.
            is ScanResult.Wifi -> TODO()
            else -> null
        }

        viewModelScope.launch {
            cancelDiscovery()
            _state.update { CameraChooserUiState.Connecting }
            connector.connect(target, requestContext)
                .fold(
                    onSuccess = {
                        logger.d { "Connected to ${it}." }
                        appPreferences.setConnectedDevice(it)
                        logger.d { "Stored $it connection to data store." }
                        _state.update { CameraChooserUiState.Connected }
                    },
                    onFailure = {
                        logger.w { "Failed to connect to ${target.serialId}" }
                        _state.update { CameraChooserUiState.Idle }
                    }
                )
        }
    }
}