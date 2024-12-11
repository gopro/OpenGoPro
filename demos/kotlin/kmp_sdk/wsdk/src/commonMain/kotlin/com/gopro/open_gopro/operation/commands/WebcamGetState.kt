package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.WebcamState
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamGetState : BaseOperation<WebcamState>("Get Webcam Status") {

    override suspend fun execute(communicator: HttpCommunicator): Result<WebcamState> =
        communicator.get { url { path("com/gopro/open_gopro/gopro/webcam/status") } }.map { it.body() }
}
