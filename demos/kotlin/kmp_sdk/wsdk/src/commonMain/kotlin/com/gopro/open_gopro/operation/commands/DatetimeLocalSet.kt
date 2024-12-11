package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.util.extensions.toUByteArray
import kotlinx.datetime.LocalDateTime


@Deprecated("Prefer to use DatetimeSet if supported on camera.")
@OptIn(ExperimentalUnsignedTypes::class)
internal class DatetimeLocalSet(val datetime: LocalDateTime) : BaseOperation<Unit>("Set Local Datetime") {
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.SET_LOCAL_DATE_TIME,
            ResponseId.Command(CommandId.SET_LOCAL_DATE_TIME),
            listOf(datetime.toUByteArray()),
        ).map { }
}
