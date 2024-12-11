package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.util.extensions.toUByte
import com.gopro.open_gopro.util.extensions.toUByteArray

internal class SetApMode(val enable: Boolean) : BaseOperation<Unit>("Set AP Mode") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.SET_AP_MODE,
            ResponseId.Command(CommandId.SET_AP_MODE),
            listOf(enable.toUByte().toUByteArray())
        ).map { }
}