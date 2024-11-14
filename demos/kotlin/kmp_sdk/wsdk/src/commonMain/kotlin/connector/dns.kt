package connector

import domain.connector.IConnector
import domain.data.ICameraRepository
import domain.network.IDnsApi
import entity.connector.ConnectionDescriptor
import entity.connector.ConnectionRequestContext
import entity.connector.GoProId
import entity.connector.NetworkType
import entity.connector.ScanResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

internal class GpDnsConnector(
    private val dnsApi: IDnsApi,
    private val cameraRepo: ICameraRepository
) : IConnector<ScanResult.Dns, ConnectionDescriptor.Http> {
    // TODO how to choose USB / WIFI here? Does it even matter?
    override val networkType = NetworkType.WIFI_WLAN

    override suspend fun scan(): Result<Flow<ScanResult.Dns>> =
        dnsApi.scan(NSD_GP_SERVICE_TYPE).map { flow ->
            flow.map { scanResult ->
                ScanResult.Dns(
                    GoProId(scanResult.serviceName.takeLast(4)),
                    scanResult.ipAddress,
                    NetworkType.WIFI_WLAN // TODO can we select between usb and wifi here?
                )
            }
        }

    override suspend fun connect(
        target: ScanResult.Dns,
        request: ConnectionRequestContext?
    ): Result<ConnectionDescriptor.Http> =
        cameraRepo.getHttpsCredentials(target.id).map { credentials ->
            ConnectionDescriptor.Http(
                id = target.id,
                ipAddress = target.ipAddress,
                port = null, // TODO can we get this?
                credentials = credentials
            )
        }


    override suspend fun disconnect(connection: ConnectionDescriptor.Http): Result<Unit> = TODO()

    companion object {
        const val NSD_GP_SERVICE_TYPE = "_gopro-web._tcp."
    }
}