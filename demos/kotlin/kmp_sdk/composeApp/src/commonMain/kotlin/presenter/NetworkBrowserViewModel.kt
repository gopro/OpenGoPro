package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import kotlinx.coroutines.launch

private val logger = Logger.withTag("CameraChooserViewModel")

sealed class NetworkBrowserType {
    data object Ble : NetworkBrowserType()
    data object Wifi : NetworkBrowserType()
    data object Dns : NetworkBrowserType()
}

class NetworkBrowserViewModel(
    private val preferences: IAppPreferences
) : ViewModel() {
    fun testDatabase() = viewModelScope.launch {

    }
}