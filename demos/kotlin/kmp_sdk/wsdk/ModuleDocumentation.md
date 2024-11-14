# Module wsdk

This is the top level WSDK module documentation.

## Usage

```kotlin
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
```