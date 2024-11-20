package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import util.extensions.toInt
import io.ktor.client.call.body
import io.ktor.http.path

internal class SetWiredControl(val enable: Boolean) :
    BaseOperation<Unit>("Set Wired Control") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/control/wired_usb")
                parameters.append("p", enable.toInt().toString())
            }
        }.map { it.body() }
}
