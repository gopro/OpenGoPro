package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import com.gopro.open_gopro.util.extensions.toInt
import io.ktor.client.call.body
import io.ktor.http.path
import com.gopro.open_gopro.operations.RequestSetTurboActive
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
