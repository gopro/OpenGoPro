package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.media.MediaList
import io.ktor.client.call.body
import io.ktor.client.statement.readBytes
import io.ktor.http.path

class MediaGetList : BaseOperation<MediaList>("Get Media List") {

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaList> =
        communicator.get { url { path("gopro/media/list") } }.map { it.body() }
}
