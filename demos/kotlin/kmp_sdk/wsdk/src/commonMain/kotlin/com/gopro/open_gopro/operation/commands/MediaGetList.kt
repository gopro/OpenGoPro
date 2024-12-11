package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.MediaList
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetList : BaseOperation<MediaList>("Get Media List") {

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaList> =
        communicator.get { url { path("com/gopro/open_gopro/gopro/media/list") } }.map { it.body() }
}
