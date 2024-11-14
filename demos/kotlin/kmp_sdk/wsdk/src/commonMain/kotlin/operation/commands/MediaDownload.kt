package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.MediaId
import io.ktor.client.statement.readBytes
import io.ktor.http.appendEncodedPathSegments
import io.ktor.http.path

internal class MediaDownload(val file: MediaId) : BaseOperation<ByteArray>("Download Media File") {

    override suspend fun execute(communicator: HttpCommunicator): Result<ByteArray> =
        communicator.get {
            url {
                path("videos/DCIM")
                appendEncodedPathSegments(file.folder)
                appendEncodedPathSegments(file.filename)
            }
        }
            // TODO wrap bytes somehow.
            .map { it.readBytes() }
}
