package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.ble.GpUuid
import util.extensions.mapFromGenericProtoResponseToResult
import entity.operation.proto.RequestCreateCOHNCert
import pbandk.encodeToByteArray

internal class CohnCreateCert(val override: Boolean):
    BaseOperation<Unit>("Create COHN Cert") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit>
        = communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.REQUEST_CREATE_COHN_CERT,
            RequestCreateCOHNCert(override).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_CREATE_COHN_CERT),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()
}
