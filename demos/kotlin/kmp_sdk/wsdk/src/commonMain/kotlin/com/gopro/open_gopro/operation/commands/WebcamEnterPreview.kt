package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamEnterPreview : BaseOperation<Unit>("Enter Webcam Preview") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get { url { path("com/gopro/open_gopro/gopro/webcam/preview") } }.map { it.body() }
}
