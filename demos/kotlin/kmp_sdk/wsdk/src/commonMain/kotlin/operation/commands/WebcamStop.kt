package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

class WebcamStop : BaseOperation<Unit>("Stop Webcam") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/webcam/stop") } }.map { it.body() }
}
