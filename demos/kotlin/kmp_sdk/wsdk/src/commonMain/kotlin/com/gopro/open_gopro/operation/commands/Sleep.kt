/* Sleep.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId

@OptIn(ExperimentalUnsignedTypes::class)
internal class Sleep : BaseOperation<Unit>("Sleep") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator.executeTlvCommand(CommandId.SLEEP, ResponseId.Command(CommandId.SLEEP)).map {}
}
