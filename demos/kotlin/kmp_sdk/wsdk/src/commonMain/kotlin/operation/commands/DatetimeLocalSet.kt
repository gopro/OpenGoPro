package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import extensions.toUByteArray
import kotlinx.datetime.LocalDateTime


@Deprecated("Prefer to use DatetimeSet if supported on camera.")
@OptIn(ExperimentalUnsignedTypes::class)
class DatetimeLocalSet(val datetime: LocalDateTime) : BaseOperation<Unit>("Set Local Datetime") {
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.SET_LOCAL_DATE_TIME,
            ResponseId.Command(CommandId.SET_LOCAL_DATE_TIME),
            listOf(datetime.toUByteArray()),
        ).map { }
}
