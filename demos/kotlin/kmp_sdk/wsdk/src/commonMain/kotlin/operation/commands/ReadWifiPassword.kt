package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import entity.network.GpUuid
import extensions.decodeToString

@OptIn(ExperimentalUnsignedTypes::class)
internal class ReadWifiPassword : BaseOperation<String>("Read Wifi Password") {
    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.readCharacteristic(GpUuid.WAP_PASSWORD.toUuid()).map { it.decodeToString() }
}