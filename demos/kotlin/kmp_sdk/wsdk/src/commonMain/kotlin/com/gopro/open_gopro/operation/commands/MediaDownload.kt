package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.MediaId
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
        }.map { it.readBytes() }
}
