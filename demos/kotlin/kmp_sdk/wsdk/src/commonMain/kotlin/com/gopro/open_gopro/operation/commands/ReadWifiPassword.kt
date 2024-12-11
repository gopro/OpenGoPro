package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.decodeToString

@OptIn(ExperimentalUnsignedTypes::class)
internal class ReadWifiPassword : BaseOperation<String>("Read Wifi Password") {
    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.readCharacteristic(GpUuid.WAP_PASSWORD.toUuid()).map { it.decodeToString() }
}