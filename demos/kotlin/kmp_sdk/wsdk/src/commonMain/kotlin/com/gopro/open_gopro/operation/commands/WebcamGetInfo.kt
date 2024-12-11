package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.WebcamInfo
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamGetInfo : BaseOperation<WebcamInfo>("Get Webcam Info") {

    override suspend fun execute(communicator: HttpCommunicator): Result<WebcamInfo> =
        communicator.get { url { path("com/gopro/open_gopro/gopro/webcam/version") } }.map { it.body() }
}
