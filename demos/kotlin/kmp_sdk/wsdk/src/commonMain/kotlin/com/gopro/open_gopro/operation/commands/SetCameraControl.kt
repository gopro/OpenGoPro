package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.CameraControlStatus
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.http.path
import com.gopro.open_gopro.operations.EnumCameraControlStatus
import com.gopro.open_gopro.operations.RequestSetCameraControlStatus
import pbandk.encodeToByteArray

internal class SetCameraControl(val status: CameraControlStatus) :
    BaseOperation<Unit>("Set Camera Control") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> {
        val request = RequestSetCameraControlStatus(
            EnumCameraControlStatus.fromValue(status.value)
        )
        return communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.SET_CAMERA_CONTROL,
            request.encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.SET_CAMERA_CONTROL_RSP),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()
    }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/control/set_ui_controller")
                parameters.append("p", status.value.toString())
            }
        }.map { it.body() }
}
