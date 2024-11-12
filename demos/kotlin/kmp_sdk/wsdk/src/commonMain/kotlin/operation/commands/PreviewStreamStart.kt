package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

class PreviewStreamStart(val port: Int? = null) :
    BaseOperation<Unit>("Start Preview Stream") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/stream/start")
                this@PreviewStreamStart.port?.let {
                    parameters.append("port", it.toString())
                }
            }
        }.map { it.body() }
}
