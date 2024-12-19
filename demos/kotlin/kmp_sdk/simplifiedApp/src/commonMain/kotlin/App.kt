import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.OgpSdkAppContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

private var isStarted = false

fun app(appContext: OgpSdkAppContext) {
    if (isStarted) return

    isStarted = true
    // Set as desired
    val dispatcher = Dispatchers.IO
    val coroutineScope = CoroutineScope(dispatcher)

    // Initialize WSDK
    val sdk = OgpSdk(dispatcher, appContext)

    coroutineScope.launch {
        // Discover and take the first device we find
        val device = sdk.discover(NetworkType.BLE).first()

        // Connect (assume success)
        val goproId = sdk.connect(device).getOrThrow()

        // Now retrieve the gopro (assume success)
        val gopro = sdk.getGoPro(goproId).getOrThrow()

        // Set the shutter
        gopro.commands.setShutter(true)
    }
}