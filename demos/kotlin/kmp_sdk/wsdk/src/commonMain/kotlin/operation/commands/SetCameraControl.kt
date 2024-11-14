package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import entity.operation.CameraControlStatus
import extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.http.path
import entity.operation.proto.EnumCameraControlStatus
import entity.operation.proto.RequestSetCameraControlStatus
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
