package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.operations.PresetGroupId
import com.gopro.open_gopro.util.extensions.toUByteArray
import io.ktor.client.call.body
import io.ktor.http.path

internal class PresetLoadGroup(private val group: PresetGroupId) : BaseOperation<Unit>("Load Preset Group") {
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
