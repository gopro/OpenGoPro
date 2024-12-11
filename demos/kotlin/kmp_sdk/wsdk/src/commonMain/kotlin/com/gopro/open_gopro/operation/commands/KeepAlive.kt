package com.gopro.open_gopro.operation.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.entity.queries.Led
import com.gopro.open_gopro.entity.queries.SettingId

internal class KeepAlive : BaseOperation<Unit>("Keep Alive") {

    @OptIn(ExperimentalUnsignedTypes::class)
    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeSetting(SettingId.LED, ubyteArrayOf(Led.KEEP_ALIVE.value)).map {}
}