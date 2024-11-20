package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import util.extensions.toUByte
import util.extensions.toUByteArray

internal class SetApMode(val enable: Boolean) : BaseOperation<Unit>("Set AP Mode") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.SET_AP_MODE,
            ResponseId.Command(CommandId.SET_AP_MODE),
            listOf(enable.toUByte().toUByteArray())
        ).map { }
}