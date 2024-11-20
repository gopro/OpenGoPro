package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import util.extensions.toLocalDateTime
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
