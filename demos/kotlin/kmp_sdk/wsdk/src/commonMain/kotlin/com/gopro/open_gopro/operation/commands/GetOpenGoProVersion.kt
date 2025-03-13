/* GetOpenGoProVersion.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.operations.OgpVersionHttpResponse
import io.github.z4kn4fein.semver.Version
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class GetOpenGoProVersion : BaseOperation<Version>("Get Open GoPro Version") {
  override suspend fun execute(communicator: BleCommunicator): Result<Version> =
      communicator
          .executeTlvCommand(
              CommandId.GET_OGP_VERSION,
              ResponseId.Command(CommandId.GET_OGP_VERSION),
          )
          .map { Version(major = it[1].toInt(), minor = it[3].toInt()) }

  override suspend fun execute(communicator: HttpCommunicator): Result<Version> =
      communicator
          .get { url { path("gopro/version") } }
          .map {
            (it.body() as OgpVersionHttpResponse).version.split(".").let { version ->
              Version(version[0].toInt(), version[1].toInt())
            }
          }
}
