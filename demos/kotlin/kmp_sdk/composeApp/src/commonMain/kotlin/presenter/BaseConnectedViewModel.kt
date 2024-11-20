package presenter

import Wsdk
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import gopro.GoPro
import kotlinx.coroutines.launch

open class BaseConnectedViewModel(
    private val appPreferences: IAppPreferences,
    private val wsdk: Wsdk,
    tag: String
) : ViewModel() {
    protected val logger = Logger.withTag(tag)

    protected lateinit var gopro: GoPro

    open fun start() {
        logger.d("Starting...")
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = wsdk.getGoPro(it)
            } ?: throw Exception("No connected device found.")
            onStart()
        }
    }

    open fun stop() {
        logger.d("Stopping...")
    }

    protected open fun onStart() {}
}