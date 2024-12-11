package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.util.extensions.toLocalDateTime
import kotlinx.datetime.LocalDateTime


@Deprecated("Prefer to use DatetimeGet if supported on camera.")
@OptIn(ExperimentalUnsignedTypes::class)
internal class DatetimeLocalGet : BaseOperation<LocalDateTime>("Get Local Datetime") {
    override suspend fun execute(communicator: BleCommunicator): Result<LocalDateTime> =
        communicator.executeTlvCommand(
            CommandId.GET_DATE_TIME,
            ResponseId.Command(CommandId.GET_LOCAL_DATE_TIME)
        ).map {
            it.toLocalDateTime()
        }
}
