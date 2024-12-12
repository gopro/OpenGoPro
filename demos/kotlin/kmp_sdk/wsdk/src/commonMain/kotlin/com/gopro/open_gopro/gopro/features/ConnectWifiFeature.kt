package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.OgpSdkIsolatedKoinContext
import com.gopro.open_gopro.domain.data.ICameraRepository
import kotlinx.coroutines.delay

/**
 * Establish a Wi-Fi connection where the camera is an Access Point
 *
 * Note! BLE must already be connected before using this feature.
 *
 * @see [Access Points](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#access-point-mode-ap)
 *
 * @property context
 */
class ConnectWifiFeature internal constructor(private val context: IFeatureContext) {
    private val cameraRepo: ICameraRepository = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()

    /**
     * Establish a Wi-Fi connection where the camera is an Access Point
     */
    suspend fun connect(): Result<Unit> {
        // Get Wifi info and enable Access Point via BLE
        val ssid = context.gopro.commands.readWifiSsid().getOrThrow()
        val password = context.gopro.commands.readWifiPassword().getOrThrow()
        context.gopro.commands.setApMode(true).getOrThrow()

        // TODO. Trying to brute force fix wifi connection delays. It seems to be working...
        // So presumably there is some come-up period where the GoPro can not connect and does
        // not gracefully disconnect.
        delay(5000)

        // Connect Wifi
        while (true) {
            context.connector.connect(
                ScanResult.Wifi(context.gopro.id, ssid),
                ConnectionRequestContext.Wifi(password)
            ).onSuccess {
                cameraRepo.addWifiCredentials(
                    context.gopro.id,
                    ssid,
                    password
                )
                val connection = ConnectionDescriptor.Http(
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