package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
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
                path("com/gopro/open_gopro/gopro/camera/presets/load")
                parameters.append("id", preset.toString())
            }
        }.map { it.body() }

}
