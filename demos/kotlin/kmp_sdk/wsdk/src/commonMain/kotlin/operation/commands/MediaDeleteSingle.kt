package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.media.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

class MediaDeleteSingle(val file: MediaId) : BaseOperation<Unit>("Delete Single Media") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/media/delete/file")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.body() }
}
