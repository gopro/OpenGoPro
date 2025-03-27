/* ConnectWifiFeature.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.OgpSdkIsolatedKoinContext
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.data.ICameraRepository
import kotlin.time.DurationUnit
import kotlin.time.toDuration
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.timeout

/**
 * Establish a Wi-Fi connection where the camera is an Access Point
 *
 * Note! BLE must already be connected before using this feature.
 *
 * @property context
 * @see
 *   [Access Points](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#access-point-mode-ap)
 */
class ConnectWifiFeature internal constructor(private val context: IFeatureContext) {
  private val cameraRepo: ICameraRepository = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()

  /** Establish a Wi-Fi connection where the camera is an Access Point */
  @OptIn(FlowPreview::class)
  suspend fun connect(): Result<Unit> {
    // Get Wifi info and enable Access Point via BLE
    val ssid = context.gopro.commands.readWifiSsid().getOrThrow()
    val password = context.gopro.commands.readWifiPassword().getOrThrow()
    context.gopro.commands.setApMode(true).getOrThrow()

    try {
      // Wait for camera wifi ready status
      context.gopro.statuses.apMode
          .registerValueUpdate()
          .getOrThrow()
          .timeout(5.toDuration(DurationUnit.SECONDS))
          .first { it }
      // TODO unregister
    } catch (e: TimeoutCancellationException) {
      return Result.failure(e)
    }

    // Connect Wifi
    while (true) {
      context.connector
          .connect(ScanResult.Wifi(context.gopro.id, ssid), ConnectionRequestContext.Wifi(password))
          .onSuccess {
            cameraRepo.addWifiCredentials(context.gopro.id, ssid, password)
            val connection =
                ConnectionDescriptor.Http(
                    id = context.gopro.id,
                    ipAddress = "10.5.5.9",
                    ssid = ssid,
                    port = 8080,
                )
            context.facadeFactory.storeConnection(connection)
            return Result.success(Unit)
          }
      // Toggle AP mode to try to recover
      context.gopro.commands.setApMode(false)
      delay(2000)
      context.gopro.commands.setApMode(true)
      delay(2000)
    }
  }
}
