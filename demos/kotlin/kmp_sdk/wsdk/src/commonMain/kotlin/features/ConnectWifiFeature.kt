package features

import WsdkIsolatedKoinContext
import domain.connector.ConnectionRequestContext
import domain.data.ICameraRepository
import entity.connector.ScanResult
import kotlinx.coroutines.delay
import kotlin.time.DurationUnit
import kotlin.time.toDuration

class ConnectWifiFeature(featureContext: IFeatureContext) : IFeatureContext by featureContext {
    private val cameraRepo: ICameraRepository = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    suspend fun connect() {
        // Get Wifi info and enable Access Point via BLE
        gopro.commands.setApMode(true).getOrThrow()
        val ssid = gopro.commands.readWifiSsid().getOrThrow()
        val password = gopro.commands.readWifiPassword().getOrThrow()

        // Connect Wifi
        // TODO finite amount of retries?
        while (true) {
            connector.connect(
                ScanResult.Wifi(gopro.serialId, ssid),
                ConnectionRequestContext.Wifi(password)
            ).onSuccess {
                cameraRepo.addWifiCredentials(
                    gopro.serialId,
                    ssid,
                    password
                )
                facadeFactory.storeConnection(it)
                return
            }
            // Toggle AP mode to try to recover
            gopro.commands.setApMode(false)
            delay(2.toDuration(DurationUnit.SECONDS))
            gopro.commands.setApMode(true)
            delay(2.toDuration(DurationUnit.SECONDS))
        }
    }
}