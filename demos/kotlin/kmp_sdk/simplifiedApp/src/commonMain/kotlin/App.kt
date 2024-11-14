import entity.connector.NetworkType
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

    // Initialize WSDK and get the top level objects
    Wsdk.init(dispatcher, appContext)
    val connector = Wsdk.getCameraConnector()
    val goproFactory = Wsdk.getGoProFactory()

    coroutineScope.launch {
        // Discover and take the first device we find
        val target = connector.discover(NetworkType.BLE).first()

        // Connect
        val goproId = connector.connect(target).getOrThrow()

        // Now retrieve the gopro
        val gopro = goproFactory.getGoPro(goproId)

        // Set the shutter
        gopro.commands.setShutter(true)
    }
}