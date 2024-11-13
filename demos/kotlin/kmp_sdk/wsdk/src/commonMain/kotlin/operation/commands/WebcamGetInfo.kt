package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.WebcamInfo
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamGetInfo : BaseOperation<WebcamInfo>("Get Webcam Info") {

    override suspend fun execute(communicator: HttpCommunicator): Result<WebcamInfo> =
        communicator.get { url { path("gopro/webcam/version") } }.map { it.body() }
}
