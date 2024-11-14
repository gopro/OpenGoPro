package connector

import domain.connector.ICameraConnector
import domain.connector.IConnector
import entity.connector.ConnectionDescriptor
import entity.connector.ConnectionRequestContext
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.merge

class CameraConnector internal constructor(
    private val bleConnector: IConnector<ScanResult.Ble, ConnectionDescriptor.Ble>,
    private val wifiConnector: IConnector<ScanResult.Wifi, ConnectionDescriptor.Http>,
    private val dnsConnector: IConnector<ScanResult.Dns, ConnectionDescriptor.Http>,
) : ICameraConnector {
    override suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> =
        networkTypes.map { networkType ->
            when (networkType) {
                NetworkType.BLE -> bleConnector
                NetworkType.WIFI_WLAN -> dnsConnector
                NetworkType.WIFI_AP -> wifiConnector
                NetworkType.USB -> dnsConnector
            }.scan().fold(
                onSuccess = { it },
                onFailure = { throw Exception(it) }
            )
        }.merge()

    override suspend fun connect(
        target: ScanResult,
        connectionRequestContext: ConnectionRequestContext?
    ): Result<ConnectionDescriptor> =
        when (target) {
            is ScanResult.Ble -> bleConnector.connect(target, connectionRequestContext)
            is ScanResult.Dns -> dnsConnector.connect(target, connectionRequestContext)
            is ScanResult.Wifi -> wifiConnector.connect(target, connectionRequestContext)
        }
}
