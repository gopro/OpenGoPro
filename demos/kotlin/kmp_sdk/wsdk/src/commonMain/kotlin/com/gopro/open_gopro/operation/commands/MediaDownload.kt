/* MediaDownload.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.MediaId
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
