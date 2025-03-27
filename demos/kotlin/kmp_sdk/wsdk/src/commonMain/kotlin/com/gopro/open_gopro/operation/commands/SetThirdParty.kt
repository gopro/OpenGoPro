package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class SetThirdParty : BaseOperation<Unit>("Set Third Party") {
  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator
          .executeTlvCommand(
              CommandId.SET_THIRD_PARTY, ResponseId.Command(CommandId.SET_THIRD_PARTY))
          .map {}

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator.get { url { path("gopro/camera/analytics/set_client_info") } }.map { it.body() }
}
