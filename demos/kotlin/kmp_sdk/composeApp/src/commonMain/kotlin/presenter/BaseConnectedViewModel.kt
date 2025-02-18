package presenter

import com.gopro.open_gopro.OgpSdk
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.gopro.GoPro
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

open class BaseConnectedViewModel(
    private val appPreferences: IAppPreferences,
    private val sdk: OgpSdk,
    tag: String
) : ViewModel() {
    protected val logger = Logger.withTag(tag)

    protected lateinit var gopro: GoPro

    private var _disconnects = MutableStateFlow<CommunicationType?>(null)
    val disconnects = _disconnects.asStateFlow()

    open fun start() {
        logger.d("Starting...")
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = sdk.getGoPro(it).getOrThrow()
            } ?: throw Exception("No connected device found.")
            viewModelScope.launch {
                gopro.disconnects.collect { disconnect ->
                    _disconnects.update { disconnect }
                }
            }
            onStart()
        }
    }

    open fun stop() {
        logger.d("Stopping...")
    }

    protected open fun onStart() {}
}