# Module Open GoPro SDK

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/gh-pages/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>
<br>
<img alt="Static Badge" src="https://img.shields.io/badge/android-android?label=platform">
<img alt="Static Badge" src="https://img.shields.io/badge/TODO-TODO">

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

## Quick Start (Demo App)

To see a simple demo app that demonstrates most of the SDK, build and load the `composeApp` project from TODO.

General usage is (TODO screenshots):

1. Select an interface to scan for GoPro's (initially only BLE will be available) and select "Scan"
    ![initial demo app](images/initial.png)
2. Click on a discovered GoPro to connect to it.
    ![initial demo app](images/scanned.png)
3. Select "Toggle Shutter" to verify communication
    ![initial demo app](images/connected.png)
4. Select "Connect Wifi" if desired
    ![initial demo app](images/connecting_wifi.png)
5. Select a submenu to enter. Note that some require HTTP so you will have needed to Connect Wifi.
    ![initial demo app](images/get_media.png)

## API Documentation

An API reference can be found below or in the side menu.

# Package com.gopro.open_gopro

This is the top level entrypoint to use the SDK. It contains components to discover, connect, and retrieve a GoPro.

# Package com.gopro.open_gopro.exceptions

todo move these into their relevant packages

# Package com.gopro.open_gopro.gopro

This package contains components that relate to the connected GoPro including methods to operate on it.

# Package com.gopro.open_gopro.operations

This package contains enums and other value containers that are used to operate on the GoPro.