package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.media.MediaId
import io.ktor.client.statement.readBytes
import io.ktor.http.path

internal class MediaGetThumbnail(val file: MediaId) : BaseOperation<ByteArray>("Get Media File Thumbnail") {

    override suspend fun execute(communicator: HttpCommunicator): Result<ByteArray> =
        communicator.get {
            url {
                path("gopro/media/thumbnail")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.readBytes() }
}
