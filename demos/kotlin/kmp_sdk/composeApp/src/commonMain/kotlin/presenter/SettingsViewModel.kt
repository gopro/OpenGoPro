package presenter

import Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import entity.queries.Fps
import entity.queries.Resolution
import entity.queries.VideoFov
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class SettingsViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk,
) : BaseConnectedViewModel(appPreferences, wsdk, "SettingsViewModel") {
    private var _currentResolution = MutableStateFlow(Resolution.RES_1080)
    val currentResolution = _currentResolution.asStateFlow()

    private var _resolutionCaps = MutableStateFlow<List<Resolution>>(listOf())
    val resolutionCaps = _resolutionCaps.asStateFlow()

    private var _currentFps = MutableStateFlow(Fps.FPS_30)
    val currentFps = _currentFps.asStateFlow()

    private var _fpsCaps = MutableStateFlow<List<Fps>>(listOf())
    val fpsCaps = _fpsCaps.asStateFlow()

    private var _currentFov = MutableStateFlow(VideoFov.WIDE)
    val currentFov = _currentFov.asStateFlow()

    private var _fovCaps = MutableStateFlow<List<VideoFov>>(listOf())
    val fovCaps = _fovCaps.asStateFlow()

    private var _currentBattery = MutableStateFlow(0)
    val currentBattery = _currentBattery.asStateFlow()

    private var _isEncoding = MutableStateFlow(false)
    val isEncoding = _isEncoding.asStateFlow()

    private var _isBusy = MutableStateFlow(false)
    val isBusy = _isBusy.asStateFlow()

    fun setResolution(resolution: Resolution) {
        viewModelScope.launch {
            gopro.settings.resolution.setValue(resolution)
        }
    }

    fun setFps(fps: Fps) {
        viewModelScope.launch {
            gopro.settings.fps.setValue(fps)
        }
    }

    fun setFov(fov: VideoFov) {
        viewModelScope.launch {
            gopro.settings.fov.setValue(fov)
        }
    }

    override fun onStart() {
        viewModelScope.launch {
            gopro.settings.resolution.registerValueUpdates().getOrThrow().let {
                it.collect { resolution -> _currentResolution.update { resolution } }
            }
        }
        viewModelScope.launch {
            gopro.settings.resolution.registerCapabilityUpdates().getOrThrow().let {
                it.collect { resolutions -> _resolutionCaps.update { resolutions } }
            }
        }
        viewModelScope.launch {
            gopro.settings.fps.registerValueUpdates().getOrThrow().let {
                it.collect { fps -> _currentFps.update { fps } }
            }
        }
        viewModelScope.launch {
            gopro.settings.fps.registerCapabilityUpdates().getOrThrow().let {
                it.collect { fpses -> _fpsCaps.update { fpses } }
            }
        }
        viewModelScope.launch {
            gopro.settings.fov.registerValueUpdates().getOrThrow().let {
                it.collect { fov -> _currentFov.update { fov } }
            }
        }
        viewModelScope.launch {
            gopro.settings.fov.registerCapabilityUpdates().getOrThrow().let {
                it.collect { fovs -> _fovCaps.update { fovs } }
            }
        }
        viewModelScope.launch {
            gopro.statuses.batteryLevel.registerValueUpdate().getOrThrow().let {
                it.collect { battery -> _currentBattery.update { battery } }
            }
        }
        // Just reuse the gopro's busy and ready. In fact we can't unregister these because the
        // facade relies on the. TODO need a layer above this to prevent this.
        viewModelScope.launch {
            gopro.isBusy.collect { isBusy -> _isBusy.update { isBusy } }
        }
        viewModelScope.launch {
            gopro.isEncoding.collect { isEncoding -> _isEncoding.update { isEncoding } }
        }
    }

    override fun stop() {
        runBlocking {
            // TODO the response to these are not routed correctly
//            gopro.settings.fov.unregisterValueUpdates()
//            gopro.settings.fps.unregisterValueUpdates()
//            gopro.settings.resolution.unregisterValueUpdates()
//            gopro.settings.resolution.unregisterCapabilityUpdates()
//            gopro.settings.fps.unregisterCapabilityUpdates()
//            gopro.settings.fov.unregisterCapabilityUpdates()
            super.stop()
        }
    }
}