package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal object Reboot : BaseOperation<Unit>("Reboot") {
  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator.executeTlvCommand(CommandId.REBOOT, ResponseId.Command(CommandId.REBOOT)).map {}

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator.get { url { path("gp/gpControl/command/system/reset") } }.map { it.body() }
}
