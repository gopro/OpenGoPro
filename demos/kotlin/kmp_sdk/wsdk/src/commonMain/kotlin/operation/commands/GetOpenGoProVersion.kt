package operation.commands

import entity.operation.OgpVersionHttpResponse
import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import io.github.z4kn4fein.semver.Version
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
class GetOpenGoProVersion : BaseOperation<Version>("Get Open GoPro Version") {
    override suspend fun execute(communicator: BleCommunicator): Result<Version> =
        communicator.executeTlvCommand(
            CommandId.GET_OGP_VERSION,
            ResponseId.Command(CommandId.GET_OGP_VERSION),
        ).map {
            Version(
                major = it[1].toInt(),
                minor = it[3].toInt()
            )
        }

    override suspend fun execute(communicator: HttpCommunicator): Result<Version> =
        communicator.get { url { path("gopro/version") } }
            .map {
                (it.body() as OgpVersionHttpResponse).version
                    .split(".")
                    .let { version ->
                        Version(version[0].toInt(), version[1].toInt())
                    }
            }
}
