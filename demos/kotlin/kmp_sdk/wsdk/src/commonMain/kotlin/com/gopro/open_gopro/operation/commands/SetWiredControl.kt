package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.util.extensions.toInt
import io.ktor.client.call.body
import io.ktor.http.path

internal class SetWiredControl(val enable: Boolean) :
    BaseOperation<Unit>("Set Wired Control") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("com/gopro/open_gopro/gopro/camera/control/wired_usb")
                parameters.append("p", enable.toInt().toString())
            }
        }.map { it.body() }
}
