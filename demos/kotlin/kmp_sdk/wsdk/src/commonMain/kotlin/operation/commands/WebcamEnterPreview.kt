package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamEnterPreview : BaseOperation<Unit>("Enter Webcam Preview") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/webcam/preview") } }.map { it.body() }
}
