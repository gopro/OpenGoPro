package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import entity.operation.PresetInfo
import entity.operation.jsonFromProto
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onCompletion
import kotlinx.coroutines.flow.onStart
import open_gopro.EnumRegisterPresetStatus
import open_gopro.NotifyPresetStatus
import open_gopro.RequestGetPresetStatus
import pbandk.ExperimentalProtoJson
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray
import pbandk.json.encodeToJsonString

@OptIn(ExperimentalProtoJson::class)
private fun NotifyPresetStatus.toPresetInfo(): PresetInfo =
    jsonFromProto.decodeFromString(this.encodeToJsonString())

internal class PresetGetInfo : BaseOperation<Flow<PresetInfo>>("Get Preset Info") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Flow<PresetInfo>> {
        lateinit var initialInfo: PresetInfo
        // First ensure the initial request is successful, returning in any fail case.
        communicator.executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.GET_PRESET_STATUS,
            RequestGetPresetStatus(
                registerPresetStatus = listOf(EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET)
            ).encodeToByteArray(),
            ResponseId.Protobuf(
                FeatureId.QUERY,
                ActionId.GET_PRESET_STATUS_RSP
            ),
            GpUuid.CQ_QUERY
        ).fold(
            onSuccess = {
                initialInfo = NotifyPresetStatus.decodeFromByteArray(it).toPresetInfo()
            },
            onFailure = { return Result.failure(it) }
        )

        // Now register with the BLE controller to receive updates
        return communicator.registerUpdate(
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.PRESET_MODIFIED_NOTIFICATION)
        ).map { flow ->
            flow
                // Map the raw protobuf response flow to the correct return type
                .map {
                    NotifyPresetStatus
                        .decodeFromByteArray(it.payload.toByteArray())
                        .toPresetInfo()
                }.onStart {
                    emit(initialInfo)
                }.onCompletion {
                    // Unregister on flow completion
                    communicator.executeProtobufCommand(
                        FeatureId.QUERY,
                        ActionId.GET_PRESET_STATUS,
                        RequestGetPresetStatus(
                            unregisterPresetStatus = listOf(
                                EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET
                            )
                        ).encodeToByteArray(),
                        ResponseId.Protobuf(
                            FeatureId.QUERY,
                            ActionId.GET_PRESET_STATUS_RSP
                        ),
                        GpUuid.CQ_QUERY
                    )
                }
        }
    }

    override suspend fun execute(communicator: HttpCommunicator): Result<Flow<PresetInfo>> =
        communicator.get {
            url { path("gopro/camera/presets/get") }
        }.map {
            flow {
                emit(it.body())
            }
        }
}
