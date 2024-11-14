package operation.commands

import domain.api.BaseOperation
import domain.communicator.HttpCommunicator
import entity.operation.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaDeleteGrouped(val group: MediaId) : BaseOperation<Unit>("Delete Media Group") {

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.get {
            url {
                path("gp/gpControl/command/storage/delete/group")
                encodedParameters.append("p", group.asPath)
            }
        }
            .map { it.body() }
}
