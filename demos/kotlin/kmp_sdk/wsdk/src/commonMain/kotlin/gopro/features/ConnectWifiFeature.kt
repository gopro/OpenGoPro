package gopro.features

import WsdkIsolatedKoinContext
import domain.data.ICameraRepository
import entity.connector.ConnectionRequestContext
import entity.connector.ScanResult
import gopro.IFeatureContext
import kotlinx.coroutines.delay
import kotlin.time.DurationUnit
import kotlin.time.toDuration

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
    private val cameraRepo: ICameraRepository = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    /**
     * Establish a Wi-Fi connection where the camera is an Access Point
     */
    suspend fun connect() {
        // Get Wifi info and enable Access Point via BLE
        context.gopro.commands.setApMode(true).getOrThrow()
        val ssid = context.gopro.commands.readWifiSsid().getOrThrow()
        val password = context.gopro.commands.readWifiPassword().getOrThrow()

        // Connect Wifi
        // TODO finite amount of retries?
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
                return
            }
            // Toggle AP mode to try to recover
            context.gopro.commands.setApMode(false)
            delay(2.toDuration(DurationUnit.SECONDS))
            context.gopro.commands.setApMode(true)
            delay(2.toDuration(DurationUnit.SECONDS))
        }
    }
}