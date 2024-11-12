package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import extensions.toInt
import io.ktor.client.call.body
import io.ktor.http.path

class SetWiredControl(val enable: Boolean) :
    BaseOperation<Unit>("Set Wired Control") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gopro/camera/control/wired_usb")
                parameters.append("p", enable.toInt().toString())
            }
        }.map { it.body() }
}
