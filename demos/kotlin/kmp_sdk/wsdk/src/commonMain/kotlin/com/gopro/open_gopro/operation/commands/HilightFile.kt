package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class HilightFile(val file: MediaId, val offsetMs: Int? = null) :
    BaseOperation<Unit>("Hilight Media File") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/media/hilight/file")
                parameters.append("path", file.asPath)
                offsetMs?.let {
                    parameters.append("ms", it.toString())
                }
            }
        }.map { it.body() }
}
