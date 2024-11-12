package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import entity.network.GpUuid
import extensions.decodeToString

@OptIn(ExperimentalUnsignedTypes::class)
class ReadWifiSsid : BaseOperation<String>("Read Wifi SSID") {
    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.readCharacteristic(GpUuid.WAP_SSID.toUuid()).map { it.decodeToString() }
}
