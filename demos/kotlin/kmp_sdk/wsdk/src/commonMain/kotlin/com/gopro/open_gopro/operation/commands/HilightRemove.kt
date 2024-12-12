package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class HilightRemove(val file: MediaId, val offsetMs: Int? = null) :
    BaseOperation<Unit>("Remove Hilight") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/media/hilight/remove")
                parameters.append("path", file.asPath)
                offsetMs?.let {
                    parameters.append("ms", it.toString())
                }
            }
        }.map { it.body() }
}
