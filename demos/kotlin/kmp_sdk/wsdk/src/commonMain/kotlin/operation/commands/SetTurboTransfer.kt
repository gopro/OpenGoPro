package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import extensions.mapFromGenericProtoResponseToResult
import extensions.toInt
import io.ktor.client.call.body
import io.ktor.http.path
import entity.operation.proto.RequestSetTurboActive
import pbandk.encodeToByteArray

internal class SetTurboTransfer(val enable: Boolean) : BaseOperation<Unit>("Set Turbo Transfer") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.SET_TURBO_MODE,
            RequestSetTurboActive(true).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.SET_TURBO_MODE_RSP),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/media/turbo_transfer")
                parameters.append("p", enable.toInt().toString())
            }
        }.map { it.body() }
}
