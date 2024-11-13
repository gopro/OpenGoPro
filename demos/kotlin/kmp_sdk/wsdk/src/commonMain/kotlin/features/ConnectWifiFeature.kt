package features

import domain.connector.ConnectionRequestContext
import entity.connector.ScanResult
import kotlinx.coroutines.delay
import kotlin.time.DurationUnit
import kotlin.time.toDuration

class ConnectWifiFeature(private val featureContext: IFeatureContext) {
    suspend fun connect() {
        // Get Wifi info and enable Access Point via BLE
        featureContext.gopro.commands.setApMode(true).getOrThrow()
        val ssid = featureContext.gopro.commands.readWifiSsid().getOrThrow()
        val password = featureContext.gopro.commands.readWifiPassword().getOrThrow()

        // Connect Wifi
        // TODO finite amount of retries?
        while (true) {
            featureContext.connector.connect(
                ScanResult.Wifi(featureContext.gopro.serialId, ssid),
                ConnectionRequestContext.Wifi(password)
            ).onSuccess {
                featureContext.cameraRepo.addWifiCredentials(
                    featureContext.gopro.serialId,
                    ssid,
                    password
                )
                featureContext.facadeFactory.storeConnection(it)
                return
            }
            // Toggle AP mode to try to recover
            featureContext.gopro.commands.setApMode(false)
            delay(2.toDuration(DurationUnit.SECONDS))
            featureContext.gopro.commands.setApMode(true)
            delay(2.toDuration(DurationUnit.SECONDS))
        }
    }
}