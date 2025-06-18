/* App.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.OgpSdkAppContext
import com.gopro.open_gopro.gopro.GoPro
import com.gopro.open_gopro.operations.VideoResolution
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

private suspend fun examples(gopro: GoPro) {
  // Print all media files
  gopro.commands.getMediaList().onSuccess {
    it.media.forEach { fileList -> fileList.files.forEach { file -> println(file.filename) } }
  }

  // Print the current resolution
  gopro.settings.videoResolution.getValue().onSuccess { println(it.name) }

  // Print all possible resolutions
  gopro.settings.videoResolution.getCapabilities().onSuccess {
    it.forEach { resolution -> println(resolution.name) }
  }

  // Set a new resolution
  check(gopro.settings.videoResolution.setValue(VideoResolution.NUM_4K).isSuccess)

  // Print asynchronous value updates
  gopro.settings.videoResolution.registerValueUpdates().onSuccess {
    it.collect { resolution -> println(resolution.name) }
  }

  // Print asynchronous capability updates
  gopro.settings.videoResolution.registerCapabilityUpdates().onSuccess {
    it.collect { resolutions -> resolutions.forEach { resolution -> println(resolution.name) } }
  }

  // Get the current battery
  gopro.statuses.internalBatteryPercentage.getValue().onSuccess { println(it) }

  // Print asynchronous value updates
  gopro.statuses.internalBatteryPercentage.registerValueUpdate().onSuccess {
    it.collect { batteryLevel -> println(batteryLevel) }
  }

  // Use access point feature
  with(gopro.features.accessPoint) {
    // Get all available access points and filter to find our target.
    val entry = scanForAccessPoints().getOrThrow().first { it.ssid == "TARGET_SSID" }
    // Start connecting to the access point..
    connectAccessPoint(entry.ssid, "password")
  }

  // Monitor disconnects
  gopro.disconnects.collect { network -> println("The ${network.name} connection has dropped!") }

  // Wait for ready
  gopro.isReady.first { it }
}
