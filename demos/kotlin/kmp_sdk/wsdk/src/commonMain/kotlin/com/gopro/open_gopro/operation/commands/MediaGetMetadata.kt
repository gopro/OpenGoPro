package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.MediaId
import com.gopro.open_gopro.operations.MediaMetadata
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetMetadata(val file: MediaId) :
    BaseOperation<MediaMetadata>("Get Media File Metadata") {

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaMetadata> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/media/info")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.body() }
}
