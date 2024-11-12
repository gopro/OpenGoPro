package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

class MediaDeleteAll : BaseOperation<Unit>("Delete All Media") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gp/gpControl/command/storage/delete/all") } }
            .map { it.body() }
}
