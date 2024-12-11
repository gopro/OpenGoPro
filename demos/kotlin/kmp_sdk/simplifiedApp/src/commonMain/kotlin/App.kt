import com.gopro.open_gopro.Wsdk
import com.gopro.open_gopro.WsdkAppContext
import com.gopro.open_gopro.entity.connector.NetworkType
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

private var isStarted = false

fun app(appContext: WsdkAppContext) {
    if (isStarted) return

    isStarted = true
    // Set as desired
    val dispatcher = Dispatchers.IO
    val coroutineScope = CoroutineScope(dispatcher)

    // Initialize WSDK
    val wsdk = Wsdk(dispatcher, appContext)

    coroutineScope.launch {
        // Discover and take the first device we find
        val target = wsdk.discover(NetworkType.BLE).first()

        // Connect
        val goproId = wsdk.connect(target).getOrThrow()

        // Now retrieve the gopro
        val gopro = wsdk.getGoPro(goproId)

        // Set the shutter
        gopro.commands.setShutter(true)
    }
}