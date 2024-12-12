package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.http.path

internal class CohnClearCert:
    BaseOperation<Unit>("Clear COHN Cert") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit>
        = communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.REQUEST_CLEAR_COHN_CERT,
            byteArrayOf(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_CLEAR_COHN_CERT),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()


    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/cohn/cert/clear") } }.map { it.body() }
}
