package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId

@OptIn(ExperimentalUnsignedTypes::class)
internal class Sleep : BaseOperation<Unit>("Sleep") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(CommandId.SLEEP, ResponseId.Command(CommandId.SLEEP)).map { }
}
