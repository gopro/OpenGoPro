package gopro.features

import WsdkIsolatedKoinContext
import domain.data.ICameraRepository
import entity.connector.ConnectionRequestContext
import entity.connector.ScanResult
import gopro.IFeatureContext
import kotlinx.coroutines.delay
import kotlin.time.DurationUnit
import kotlin.time.toDuration

class ConnectWifiFeature internal constructor(private val context: IFeatureContext) {
    private val cameraRepo: ICameraRepository = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    suspend fun connect() {
        // Get Wifi info and enable Access Point via BLE
        context.gopro.commands.setApMode(true).getOrThrow()
        val ssid = context.gopro.commands.readWifiSsid().getOrThrow()
        val password = context.gopro.commands.readWifiPassword().getOrThrow()

        // Connect Wifi
        // TODO finite amount of retries?
        while (true) {
            context.connector.connect(
                ScanResult.Wifi(context.gopro.serialId, ssid),
                ConnectionRequestContext.Wifi(password)
            ).onSuccess {
                cameraRepo.addWifiCredentials(
                    context.gopro.serialId,
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