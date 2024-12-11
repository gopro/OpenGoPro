package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.decodeToString

@OptIn(ExperimentalUnsignedTypes::class)
internal class ReadWifiSsid : BaseOperation<String>("Read Wifi SSID") {
    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.readCharacteristic(GpUuid.WAP_SSID.toUuid()).map { it.decodeToString() }
}
