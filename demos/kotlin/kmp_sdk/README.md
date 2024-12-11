# Open GoPro Kotlin Multiplatform SDK

![Static Badge](https://img.shields.io/badge/TODO-TODO)
![Static Badge](https://img.shields.io/badge/ADD-ADD)
![Static Badge](https://img.shields.io/badge/BADGES-BADGES)

Note! This contains only an overview of the package and developer information.
Complete [Dokka](https://github.com/Kotlin/dokka)-based documentation for the OGP KMP SDK can be
found on Open GoPro TODO link.

## Overview

The Open GoPro (OGP) Kotlin Multiplatform (KMP) SDK provides a simple Coroutines-powered API to
connect to GoPro's and exercise the Open GoPro [Bluetooth Low Energy](https://gopro.github.io/OpenGoPro/ble/) 
and Wi-Fi / USB [HTTP](https://gopro.github.io/OpenGoPro/http) APIs. 

> Currently only Android is fully supported. iOS is mostly untested but there are plans to fully support it 
> soon.

## Features

- High-level GoPro class interface to use BLE and WiFi
- Supports all commands, settings, and statuses from the Open GoPro API
- Coroutines based
- Automatically handles connection maintenance:
    - manage camera ready / encoding
    - periodically sends keep alive signals
- Includes detailed logging for each module
- Includes basic demo App to show all contained functionality:
    - Capture media
    - Inspect / configure settings and statuses
    - Basic streaming
    - Setting up Camera-on-the-home-network and Livestreaming
    - Media Access and display

## Setup

### Gradle

TODO

### Permissions

TODO 

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

## Development

# Package com.gopro.open_gopro