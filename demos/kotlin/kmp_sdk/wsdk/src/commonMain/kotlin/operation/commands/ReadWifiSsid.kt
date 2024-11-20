package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import entity.network.ble.GpUuid
import util.extensions.decodeToString

@OptIn(ExperimentalUnsignedTypes::class)
internal class ReadWifiSsid : BaseOperation<String>("Read Wifi SSID") {
    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.readCharacteristic(GpUuid.WAP_SSID.toUuid()).map { it.decodeToString() }
}
