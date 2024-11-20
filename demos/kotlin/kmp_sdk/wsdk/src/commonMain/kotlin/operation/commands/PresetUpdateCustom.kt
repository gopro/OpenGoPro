package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.ble.GpUuid
import entity.operation.UpdateCustomPresetRequest
import util.extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.http.path
import entity.operation.proto.EnumPresetIcon
import entity.operation.proto.EnumPresetTitle
import entity.operation.proto.RequestCustomPresetUpdate
import pbandk.encodeToByteArray

internal class UpdateCustomPresetIcon(val icon: EnumPresetIcon) :
    BaseOperation<Unit>("Update Custom Preset Icon") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.REQUEST_PRESET_UPDATE_CUSTOM,
            RequestCustomPresetUpdate(iconId = icon).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_PRESET_UPDATE_CUSTOM),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            contentType(ContentType.Application.Json)
            url { path("gopro/camera/presets/update_custom") }
            setBody(UpdateCustomPresetRequest(iconId = icon.value))
        }.map { it.body() }
}

internal class UpdateCustomPresetTitle(val titleId: EnumPresetTitle) :
    BaseOperation<Unit>("Update Custom Preset Title") {

    private var customTitle: String? = null

    constructor(title: String) : this(EnumPresetTitle.PRESET_TITLE_CUSTOM) {
        customTitle = title
    }

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.REQUEST_PRESET_UPDATE_CUSTOM,
            RequestCustomPresetUpdate(
                titleId = titleId,
                customName = customTitle
            ).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_PRESET_UPDATE_CUSTOM),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            contentType(ContentType.Application.Json)
            url { path("gopro/camera/presets/update_custom") }
            setBody(
                UpdateCustomPresetRequest(
                    titleId = titleId.value,
                    name = customTitle
                )
            )
        }.map { it.body() }
}
