package features

import domain.connector.ConnectionRequestContext
import entity.connector.ScanResult
import kotlinx.coroutines.delay
import kotlin.time.DurationUnit
import kotlin.time.toDuration

class ConnectWifiFeature(private val featureContext: FeatureContext) {
    suspend fun connect() {
        // Get Wifi info and enable Access Point via BLE
        featureContext.commands.setApMode(true).getOrThrow()
        val ssid = featureContext.commands.readWifiSsid().getOrThrow()
        val password = featureContext.commands.readWifiPassword().getOrThrow()

        // Connect Wifi
        // TODO finite amount of retries?
        while (true) {
            featureContext.connector.connect(
                ScanResult.Wifi(featureContext.serialId, ssid),
                ConnectionRequestContext.Wifi(password)
            ).onSuccess {
                featureContext.cameraRepo.addWifiCredentials(
                    featureContext.serialId,
                    ssid,
                    password
                )
                featureContext.facadeFactory.storeConnection(it)
                return
            }
            // Toggle AP mode to try to recover
            featureContext.commands.setApMode(false)
            delay(2.toDuration(DurationUnit.SECONDS))
            featureContext.commands.setApMode(true)
            delay(2.toDuration(DurationUnit.SECONDS))
        }
    }
}