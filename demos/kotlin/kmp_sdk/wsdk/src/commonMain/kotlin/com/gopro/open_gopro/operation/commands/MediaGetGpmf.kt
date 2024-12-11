package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaGetGpmf(val file: MediaId) : BaseOperation<Unit>("Get Media File GPMF") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/media/gpmf")
                encodedParameters.append("path", file.asPath)
            }
        }
            .map { it.body() }
}
