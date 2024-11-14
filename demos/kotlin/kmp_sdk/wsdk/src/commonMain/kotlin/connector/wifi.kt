package connector


import domain.connector.IConnector
import domain.network.IWifiApi
import entity.connector.ConnectionDescriptor
import entity.connector.ConnectionRequestContext
import entity.connector.GoProId
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

internal class GpWifiConnector(private val wifiApi: IWifiApi) :
    IConnector<ScanResult.Wifi, ConnectionDescriptor.Http> {
    override val networkType = NetworkType.WIFI_AP

    override suspend fun scan(): Result<Flow<ScanResult.Wifi>> =
        wifiApi.scanForSsid().map {
            it.map { id -> ScanResult.Wifi(GoProId(id), "NAME_TODO") }
        }

    override suspend fun connect(
        target: ScanResult.Wifi,
        request: ConnectionRequestContext?
    ): Result<ConnectionDescriptor.Http> =
        when (request) {
            is ConnectionRequestContext.Wifi -> wifiApi.connect(target.ssid, request.password).map {
                // The only Wifi AP use case is direct to camera so ip address and port are hardcoded.
                ConnectionDescriptor.Http(
                    ipAddress = GP_WIFI_AP_IP_ADDRESS,
                    port = GP_WIFI_AP_PORT,
                    id = target.id
                )
            }

            else -> throw Exception("Wifi connect requires password")
        }

    override suspend fun disconnect(connection: ConnectionDescriptor.Http): Result<Unit> = TODO()

    companion object {
        const val GP_WIFI_AP_IP_ADDRESS = "10.5.5.9"
        const val GP_WIFI_AP_PORT = 8080
    }
}