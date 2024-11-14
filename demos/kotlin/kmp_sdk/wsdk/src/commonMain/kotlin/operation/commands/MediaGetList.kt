package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.MediaList
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetList : BaseOperation<MediaList>("Get Media List") {

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaList> =
        communicator.get { url { path("gopro/media/list") } }.map { it.body() }
}
