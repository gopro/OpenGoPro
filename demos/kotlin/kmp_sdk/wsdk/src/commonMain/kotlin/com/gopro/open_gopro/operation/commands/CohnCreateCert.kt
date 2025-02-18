package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import com.gopro.open_gopro.operations.RequestCreateCOHNCert
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
