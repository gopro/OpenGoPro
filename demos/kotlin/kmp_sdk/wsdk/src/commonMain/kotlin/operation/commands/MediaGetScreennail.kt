package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.media.MediaId
import io.ktor.client.call.body
import io.ktor.client.statement.readBytes
import io.ktor.http.path

class MediaGetScreennail(val file: MediaId) : BaseOperation<ByteArray>("Get Media File Screennail") {

    override suspend fun execute(communicator: HttpCommunicator): Result<ByteArray> =
        communicator.get {
            url {
                path("gopro/media/screennail")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.readBytes() }
}
