package operation.commands

import entity.operation.CohnStatus
import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import entity.operation.proto.NotifyCOHNStatus
import entity.operation.proto.RequestGetCOHNStatus
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private fun NotifyCOHNStatus.toCohnStatus(): CohnStatus =
    CohnStatus(
        status = this.status,
        ssid = this.ssid,
        state = this.state,
        password = this.password,
        username = this.username,
        ipAddress = this.ipaddress,
        macAddress = this.macaddress,
        isEnabled = this.enabled
    )

internal class CohnGetStatus :
    BaseOperation<Flow<CohnStatus>>("Get COHN Status") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Flow<CohnStatus>> {
        lateinit var initialStatue: NotifyCOHNStatus
        // First send the register command over the air
        communicator.executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.REQUEST_GET_COHN_STATUS,
            RequestGetCOHNStatus(true).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_STATUS),
            GpUuid.CQ_QUERY
        ).fold(
            onSuccess = {
                initialStatue = NotifyCOHNStatus.decodeFromByteArray(it).also {
                    // TODO check error status here. I'm not sure which one we want.
                }
            },
            onFailure = { return Result.failure(it) }
        )

        // Now register to receive notifications
        return communicator.registerUpdate(
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_STATUS),
        ).map { flow ->
            flow.map {
                NotifyCOHNStatus.decodeFromByteArray(it.payload.toByteArray()).toCohnStatus()
            }.onStart {
                emit(initialStatue.toCohnStatus())
            }
        }
    }

    override suspend fun execute(communicator: HttpCommunicator): Result<Flow<CohnStatus>> =
        communicator.get { url { path("GoProRootCA.crt") } }.map { it.body() }
}



