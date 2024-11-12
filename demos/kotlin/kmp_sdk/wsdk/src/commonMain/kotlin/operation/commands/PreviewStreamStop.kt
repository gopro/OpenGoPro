package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

class PreviewStreamStop : BaseOperation<Unit>("Stop Preview Stream") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/camera/stream/stop") } }.map { it.body() }
}
