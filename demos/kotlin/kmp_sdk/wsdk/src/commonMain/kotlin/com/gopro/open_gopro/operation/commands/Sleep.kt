package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId

@OptIn(ExperimentalUnsignedTypes::class)
internal class Sleep : BaseOperation<Unit>("Sleep") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(CommandId.SLEEP, ResponseId.Command(CommandId.SLEEP)).map { }
}
