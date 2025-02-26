/* SettingsViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.FramesPerSecond
import com.gopro.open_gopro.operations.VideoLens
import com.gopro.open_gopro.operations.VideoResolution
import data.IAppPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class SettingsViewModel(
    appPreferences: IAppPreferences,
    sdk: OgpSdk,
) : BaseConnectedViewModel(appPreferences, sdk, "SettingsViewModel") {
  private var _currentResolution = MutableStateFlow(VideoResolution.NUM_1080)
  val currentResolution = _currentResolution.asStateFlow()

  private var _resolutionCaps = MutableStateFlow<List<VideoResolution>>(listOf())
  val resolutionCaps = _resolutionCaps.asStateFlow()

  private var _currentFps = MutableStateFlow(FramesPerSecond.NUM_30_0)
  val currentFps = _currentFps.asStateFlow()

  private var _fpsCaps = MutableStateFlow<List<FramesPerSecond>>(listOf())
  val fpsCaps = _fpsCaps.asStateFlow()

  private var _currentFov = MutableStateFlow(VideoLens.WIDE)
  val currentFov = _currentFov.asStateFlow()

  private var _fovCaps = MutableStateFlow<List<VideoLens>>(listOf())
  val fovCaps = _fovCaps.asStateFlow()

  private var _currentBattery = MutableStateFlow(0)
  val currentBattery = _currentBattery.asStateFlow()

  private var _isEncoding = MutableStateFlow(false)
  val isEncoding = _isEncoding.asStateFlow()

  private var _isBusy = MutableStateFlow(false)
  val isBusy = _isBusy.asStateFlow()

  fun setResolution(resolution: VideoResolution) {
    viewModelScope.launch { gopro.settings.videoResolution.setValue(resolution) }
  }

  fun setFps(fps: FramesPerSecond) {
    viewModelScope.launch { gopro.settings.framesPerSecond.setValue(fps) }
  }

  fun setFov(fov: VideoLens) {
    viewModelScope.launch { gopro.settings.videoLens.setValue(fov) }
  }

  override fun onStart() {
    viewModelScope.launch {
      gopro.settings.videoResolution.registerValueUpdates().getOrThrow().let {
        it.collect { resolution -> _currentResolution.update { resolution } }
      }
    }
    viewModelScope.launch {
      gopro.settings.videoResolution.registerCapabilityUpdates().getOrThrow().let {
        it.collect { resolutions -> _resolutionCaps.update { resolutions } }
      }
    }
    viewModelScope.launch {
      gopro.settings.framesPerSecond.registerValueUpdates().getOrThrow().let {
        it.collect { fps -> _currentFps.update { fps } }
      }
    }
    viewModelScope.launch {
      gopro.settings.framesPerSecond.registerCapabilityUpdates().getOrThrow().let {
        it.collect { fpses -> _fpsCaps.update { fpses } }
      }
    }
    viewModelScope.launch {
      gopro.settings.videoLens.registerValueUpdates().getOrThrow().let {
        it.collect { fov -> _currentFov.update { fov } }
      }
    }
    viewModelScope.launch {
      gopro.settings.videoLens.registerCapabilityUpdates().getOrThrow().let {
        it.collect { fovs -> _fovCaps.update { fovs } }
      }
    }
    viewModelScope.launch {
      gopro.statuses.internalBatteryPercentage.registerValueUpdate().getOrThrow().let {
        it.collect { battery -> _currentBattery.update { battery } }
      }
    }
    // Just reuse the gopro's busy and ready. In fact we can't unregister these because the
    // facade relies on the. TODO need a layer above this to prevent this.
    viewModelScope.launch { gopro.isBusy.collect { isBusy -> _isBusy.update { isBusy } } }
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
