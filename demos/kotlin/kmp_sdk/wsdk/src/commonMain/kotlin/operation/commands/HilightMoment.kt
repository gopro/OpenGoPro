package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class HilightMoment : BaseOperation<Unit>("Hilight Moment") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeTlvCommand(
            CommandId.HILGIHT_MOMENT,
            ResponseId.Command(CommandId.HILGIHT_MOMENT)
        ).map { }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/media/hilight/moment") } }.map { it.body() }
}
