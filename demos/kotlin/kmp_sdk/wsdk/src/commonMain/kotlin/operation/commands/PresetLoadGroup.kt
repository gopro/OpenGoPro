package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import entity.constants.PresetGroup
import extensions.toUByteArray
import io.ktor.client.call.body
import io.ktor.http.path

internal class PresetLoadGroup(private val group: PresetGroup) : BaseOperation<Unit>("Load Preset Group") {
    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.LOAD_PRESET_GROUP,
            ResponseId.Command(CommandId.LOAD_PRESET_GROUP),
            listOf(group.value.toUByteArray()),
        ).map { Unit }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/presets/set_group")
                parameters.append("id", group.value.toInt().toString())
            }
        }.map { it.body() }


}
