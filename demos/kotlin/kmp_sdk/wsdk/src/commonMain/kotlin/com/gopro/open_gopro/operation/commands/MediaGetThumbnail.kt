package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.MediaId
import io.ktor.client.statement.readBytes
import io.ktor.http.path

internal class MediaGetThumbnail(val file: MediaId) : BaseOperation<ByteArray>("Get Media File Thumbnail") {

    override suspend fun execute(communicator: HttpCommunicator): Result<ByteArray> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/media/thumbnail")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.readBytes() }
}
