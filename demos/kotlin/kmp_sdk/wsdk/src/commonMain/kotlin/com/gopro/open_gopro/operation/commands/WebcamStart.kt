package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.entity.operation.WebcamFov
import com.gopro.open_gopro.entity.operation.WebcamProtocol
import com.gopro.open_gopro.entity.operation.WebcamResolution
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamStart(
    val resolution: WebcamResolution? = null,
    val fov: WebcamFov? = null,
    val port: Int? = null,
    val protocol: WebcamProtocol? = null
) :
    BaseOperation<Unit>("Start Webcam") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/webcam/start")
                resolution?.let {
                    parameters.append("res", it.value.toString())
                }
                fov?.let {
                    parameters.append("fov", it.value.toString())
                }
                this@WebcamStart.port?.let {
                    parameters.append("port", it.toString())
                }
                this@WebcamStart.protocol?.let {
                    parameters.append("protocol", it.value)
                }
            }
        }.map { it.body() }
}
