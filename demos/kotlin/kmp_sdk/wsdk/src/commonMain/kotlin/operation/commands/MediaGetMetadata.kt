package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.MediaId
import entity.operation.MediaMetadata
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetMetadata(val file: MediaId) :
    BaseOperation<MediaMetadata>("Get Media File Metadata") {

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaMetadata> =
        communicator.get {
            url {
                path("gopro/media/info")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.body() }
}
