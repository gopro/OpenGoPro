/* CameraViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package presenter

import androidx.lifecycle.viewModelScope
import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.operations.CohnState
import data.IAppPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class Busy(val text: String)

class CameraViewModel(
    appPreferences: IAppPreferences,
    sdk: OgpSdk,
) : BaseConnectedViewModel(appPreferences, sdk, "CameraChooserViewModel") {
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
