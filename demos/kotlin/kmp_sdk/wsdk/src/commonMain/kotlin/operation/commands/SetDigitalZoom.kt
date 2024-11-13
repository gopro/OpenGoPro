package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

internal class SetDigitalZoom(val zoom: Int) :
    BaseOperation<Unit>("Set Digital Zoom") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/digital_zoom")
                parameters.append("percent", zoom.toString())
            }
        }.map { it.body() }
}
