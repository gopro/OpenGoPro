package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import io.ktor.client.call.body
import io.ktor.http.path

internal class PresetLoad(private val preset: Int) : BaseOperation<Unit>("Load Preset") {
    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.LOAD_PRESET,
            ResponseId.Command(CommandId.LOAD_PRESET),
            listOf(ubyteArrayOf(preset.toUByte())),
        ).map { Unit }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/presets/load")
                parameters.append("id", preset.toString())
            }
        }.map { it.body() }

}
