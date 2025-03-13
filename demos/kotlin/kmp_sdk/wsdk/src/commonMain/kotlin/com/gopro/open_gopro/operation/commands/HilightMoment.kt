/* HilightMoment.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class HilightMoment : BaseOperation<Unit>("Hilight Moment") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator
          .executeTlvCommand(CommandId.HILGIHT_MOMENT, ResponseId.Command(CommandId.HILGIHT_MOMENT))
          .map {}

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator.get { url { path("gopro/media/hilight/moment") } }.map { it.body() }
}
