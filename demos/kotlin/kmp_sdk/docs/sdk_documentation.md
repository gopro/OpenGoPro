# Module Open GoPro SDK

## Usage 

```kotlin
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
```

# Package com.gopro.open_gopro

todo

# Package com.gopro.open_gopro.exceptions

todo move these into their relevant packages

# Package com.gopro.open_gopro.gopro

todo

# Package com.gopro.open_gopro.operations

todo