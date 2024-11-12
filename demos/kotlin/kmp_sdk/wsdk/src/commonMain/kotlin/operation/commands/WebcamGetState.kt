package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.WebcamState
import io.ktor.client.call.body
import io.ktor.http.path

class WebcamGetState : BaseOperation<WebcamState>("Get Webcam Status") {

    override suspend fun execute(communicator: HttpCommunicator): Result<WebcamState> =
        communicator.get { url { path("gopro/webcam/status") } }.map { it.body() }
}
