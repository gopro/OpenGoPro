package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import entity.queries.SettingId

internal class KeepAlive : BaseOperation<Unit>("Keep Alive") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeSetting(SettingId.LED, ubyteArrayOf(0x42U)).map {}
}