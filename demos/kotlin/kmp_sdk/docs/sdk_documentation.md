# Module Open GoPro SDK

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/gh-pages/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>

Welcome to the API Documentation for the [Open GoPro Kotlin Multi-platform SDK](TODO link to Maven).

This document is strictly about library usage. For a high level overview and a demo app, see
the OGP KMP SDK on [Github](https://github.com/gopro/OpenGoPro/tree/main/demos/kotlin/kmp_sdk).

The general procedure is:

1. Initialize the SDK
   ```kotlin
    // App context is platform-specific context passed from application
    val sdk = OgpSdk(Dispatchers.IO, appContext)
   ```
2. Discover and connect to a GoPro Device. A successful connection will store it in the SDK's (runtime) database.
   ```kotlin
    // Discover and take the first device we find
    val device = sdk.discover(NetworkType.BLE).first()

    // Connect (assume success)
    val goproId = sdk.connect(device).getOrThrow()
    ```

3. Now that the device is connected and stored in the SDK, retrieve the GoPro object from the SDK. This can be done any
   number of times after connection.
   ```kotlin
    // Now retrieve the gopro (assume success)
    val gopro = sdk.getGoPro(goproId).getOrThrow()
   ```
4. Manipulate the retrieved GoPro as desired
   ```kotlin
    // Set the shutter
    gopro.commands.setShutter(true)
   ```

See the relevant packages below for more detailed information on specific objects.

# Package com.gopro.open_gopro

This is the top level entrypoint to use the SDK. It contains components to discover, connect, and retrieve a
[GoPro](com.gopro.open_gopro.gopro.GoPro).

## SDK Initialization

Before performing any operations, the SDK must first be initialized with a desired coroutine scope and a platform-specific
[OgpSdkAppContext].

```kotlin
// App context is platform-specific context passed from application
val sdk = OgpSdk(Dispatchers.IO, appContext)
```

## GoPro Identifier

GoPro devices on all network mediums and their resulting [GoPro](com.gopro.open_gopro.gopro.GoPro) objects are always identified by a [GoProId] which
consists of the last 4 digits of the serial number.

## SDK Overview

The SDK maintains a run-time database of [GoPro](com.gopro.open_gopro.gopro.GoPro) objects that can be retrieved by [GoProId]. It manages storing network
connections (identified by [GoProId]) and binding / unbinding these to [GoPro](com.gopro.open_gopro.gopro.GoPro) objects as needed.

It is the user's responsibility to establish a connection via [OgpSdk.connect]. The SDK will then bind this to any
existing [GoPro](com.gopro.open_gopro.gopro.GoPro) objects

At any time the user can use [OgpSdk.getGoPro] to retrieve a [GoPro](com.gopro.open_gopro.gopro.GoPro) which will be bound to all available network connections.

## Discovering

The first step to connecting is to discover a GoPro device via [OgpSdk.discover]:

```kotlin
// Discover and take the first device we find
val device = sdk.discover(NetworkType.BLE).first()
```

> Note that the user can freely choose any combination of network types.

## Connecting

Discovered devices can be connected to via [OgpSdk.connect]

```kotlin
// Connect (assume success)
val goproId = sdk.connect(device).getOrThrow()
```

On success, the SDK will store this connection and bind to any pre-existing [GoPro](com.gopro.open_gopro.gopro.GoPro) objects.

## GoPro Retrieval

At any time, the user can attempt to retrieve a [GoPro](com.gopro.open_gopro.gopro.GoPro) object (by its [GoProId]) via [OgpSdk.getGoPro]:

```kotlin
val gopro = sdk.getGoPro(goproId)
```

This will succeed as long as their is at least one available network connection. If there are no available network
connections, a [DeviceNotFound] exception will be returned in the `Failure` result and the user must establish a
connection before proceeding.

For information on how to work with the retrieved [GoPro](com.gopro.open_gopro.gopro.GoPro), see the GoPro package TODO link.

# Package com.gopro.open_gopro.gopro

This package contains components that relate to the connected [GoPro] including methods to operate on it.

All objects here should be accessed as properties of a [GoPro] object returned from [OgpSdk.getGoPro](com.gopro.open_gopro.OgpSdk.getGoPro)

> Note that for all methods here, the return value will always be wrapped in
> a [Result](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/).

## Commands

Commands are accessed in a [CommandsContainer] via [GoPro.commands].

For example, to print all files from the media list:

```kotlin
gopro.commands.getMediaList().onSuccess {
    it.media.forEach { fileList ->
        fileList.files.forEach { file ->
            println(file.filename)
        }
    }
}
```

## Settings

Settings are accessed in a [SettingsContainer] via [GoPro.settings]. Each setting has several methods of interaction
as defined in [Setting].

For example...

- To print the current resolution

    ```kotlin
    gopro.settings.videoResolution.getValue().onSuccess { println(it.name) }
    ```

- To print all currently available resolutions:

    ```kotlin
    gopro.settings.videoResolution.getCapabilities().onSuccess {
        it.forEach { resolution ->
            println(resolution.name)
        }
    }
    ```

- To set the video resolution to a new value (assuming it is currently available):

    ```kotlin
    check(gopro.settings.videoResolution.setValue(VideoResolution.NUM_4K).isSuccess)
    ```

- To register for, collect, and print resolution value updates as they asynchronously occur:

    ```kotlin
    gopro.settings.videoResolution.registerValueUpdates().onSuccess {
        it.collect { resolution ->
            println(resolution.name)
        }
    }
    ```

- To register for, collect, and print resolution capability updates as they asynchronously occur:

    ```kotlin
    gopro.settings.videoResolution.registerCapabilityUpdates().onSuccess {
        it.collect { resolutions ->
            resolutions.forEach { resolution ->
                println(resolution.name)
            }
        }
    }
    ```

## Statuses

Statuses are accessed in a [StatusesContainer] via [GoPro.statuses]. Each status has several methods of interaction
as defined in [Status].

For example...

- To get the current battery level:

    ```kotlin
    gopro.statuses.internalBatteryPercentage.getValue().onSuccess { println(it) }
    ```

- To register for, collect, and print battery value updates as they asynchronously occur:

    ```kotlin
    gopro.statuses.internalBatteryPercentage.registerValueUpdate().onSuccess {
        it.collect { batteryLevel ->
            println(batteryLevel)
        }
    }
    ```

## Features

Features are higher layer abstractions of other API elements.
They are accessed in a [FeaturesContainer] via [GoPro.features]

Here is a (naive) example of using the [AccessPointFeature] to connect the GoPro to a Wi-Fi access point:

```kotlin
with(gopro.features.accessPoint) {
    // Get all available access points and filter to find our target.
    val entry = scanForAccessPoints().getOrThrow().first { it.ssid == "TARGET_SSID" }
    // Start connecting to the access point..
    connectAccessPoint(entry.ssid, "password")
}
```

## Observation

Besides any of the flows returned from the various API elements above, there are several properties that can be observed
as defined in [IGpDescriptor].

For example...

- To monitor disconnects:

    ```kotlin
    gopro.disconnects.collect { network ->
        println("The ${network.name} connection has dropped!")
    }
    ```

- To wait until the camera is ready to perform an operation...

    ```kotlin
    gopro.isReady.first { it }
    ```

    > Note that the [GoPro] object itself already monitors this and will suspend any requested operations until the camera
    > is ready. That is, the user does not need to track this manually.

# Package com.gopro.open_gopro.operations

This package contains enums and other data entities that are used to operate on the GoPro.
