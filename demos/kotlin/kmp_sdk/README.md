# Open GoPro Kotlin Multiplatform SDK

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/gh-pages/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>
<br>
<img alt="Static Badge" src="https://img.shields.io/badge/android-android?label=platform">
<img alt="Static Badge" src="https://img.shields.io/badge/TODO-TODO">

## Overview

The Open GoPro (OGP) Kotlin Multiplatform (KMP) SDK provides a simple Coroutines-powered API to
connect to GoPro cameras and exercise the Open GoPro [Bluetooth Low Energy](https://gopro.github.io/OpenGoPro/ble/)
and Wi-Fi / USB [HTTP](https://gopro.github.io/OpenGoPro/http) APIs.

> Currently only Android is fully supported. iOS is mostly untested but there are plans to fully support it
> soon.

## Features

- High-level GoPro class interface to use BLE and WiFi
- Supports all commands, settings, and statuses from the [Open GoPro](https://gopro.github.io/OpenGoPro/) API
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

The OGP KMP SDK can be setup via Gradle as:

#### Version Catalog

```toml
[versions]
ogpSdk = "0.1.0"
agp = "8.7.2"
kotlin = "2.0.10"

[libraries]
openGopro = { module = "TODO_NAMESPACE:open-gopro", version.ref = "ogpSdk"}

[plugins]
androidApplication = { id = "com.android.application", version.ref = "agp" }
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
```

#### Gradle Build

```Gradle
plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.kotlinMultiplatform)
}

repositories {
    mavenCentral()
}

kotlin {
    androidTarget()

    sourceSets {
        commonMain.dependencies {
            implementation(libs.openGopro)
        }
    }
}

android {
    // ...
}
```

### Permissions

The SDK needs permissions relating to Bluetooth, WiFi, and disc writing.

#### Android

You can find an example in the demo app:
- TODO link to XML
- TODO link to run-time request code

## Quick Start (Demo App)

To see a simple demo app that demonstrates most of the SDK, build and load the `composeApp` project from TODO.

General usage is (TODO screenshots):

1. Select an interface to scan for GoPro's (initially only BLE will be available) and select "Scan"
    <br>![initial demo app](docs/assets/initial.png)
2. Click on a discovered GoPro to connect to it.
    ![initial demo app](docs/assets/scanned.png)
3. Select "Toggle Shutter" to verify communication
    ![initial demo app](docs/assets/connected.png)
4. Select "Connect Wifi" if desired
    ![initial demo app](docs/assets/connecting_wifi.png)
5. Select a submenu to enter. Note that some require HTTP so you will have needed to Connect Wifi.
    ![initial demo app](docs/assets/get_media.png)

## Usage

> Note! This section contains only an overview.
> Complete API documentation for the OGP KMP SDK can be found on Open GoPro TODO link.

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

TODO