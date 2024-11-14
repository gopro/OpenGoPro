package connector

import co.touchlab.kermit.Logger
import domain.connector.ConnectionRequestContext
import domain.connector.IConnector
import domain.network.IBleApi
import entity.connector.ConnectionDescriptor
import entity.connector.NetworkType
import entity.connector.ScanResult
import entity.network.BleAdvertisement
import entity.network.GpUuid
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import org.koin.core.component.KoinComponent

private val notifiableUuids = listOf(
    GpUuid.CQ_COMMAND_RESP,
    GpUuid.CQ_QUERY_RESP,
    GpUuid.CQ_SETTINGS_RESP,
    GpUuid.CN_NET_MGMT_RESP
).map { it.toUuid() }.toSet()

internal class GpBleConnector(private val bleApi: IBleApi) :
    IConnector<ScanResult.Ble, ConnectionDescriptor.Ble>, KoinComponent {
    override val networkType = NetworkType.BLE

    private val idAdvMap = mutableMapOf<String, BleAdvertisement>()

    override suspend fun scan(): Result<Flow<ScanResult.Ble>> =
        bleApi.scan(setOf(GpUuid.S_CONTROL_QUERY.toUuid())).map { flow ->
            flow.filter { it.name != null }
                .onStart { idAdvMap.clear() }
                .onEach { idAdvMap[it.name!!.takeLast(4)] = it }
                .map { ScanResult.Ble(it.name!!.takeLast(4), it.id, it.name ?: "") }
        }


    override suspend fun connect(
        target: ScanResult.Ble,
        request: ConnectionRequestContext?
    ): Result<ConnectionDescriptor.Ble> =
        bleApi.connect(idAdvMap.getValue(target.serialId)).fold(
            onFailure = { return Result.failure(it) },
            onSuccess = { device ->
                bleApi.enableNotifications(device, notifiableUuids)
                    .map { ConnectionDescriptor.Ble(target.serialId, device) }
            }
        )

    override suspend fun disconnect(connection: ConnectionDescriptor.Ble): Result<Unit> =
        bleApi.disconnect(connection.device)
}
