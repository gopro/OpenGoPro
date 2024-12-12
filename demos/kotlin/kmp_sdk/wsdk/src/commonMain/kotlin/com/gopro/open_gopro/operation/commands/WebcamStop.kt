package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamStop : BaseOperation<Unit>("Stop Webcam") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("gopro/webcam/stop") } }.map { it.body() }
}
