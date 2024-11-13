package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.media.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetGpmf(val file: MediaId) : BaseOperation<Unit>("Get Media File GPMF") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/media/gpmf")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.body() }
}
