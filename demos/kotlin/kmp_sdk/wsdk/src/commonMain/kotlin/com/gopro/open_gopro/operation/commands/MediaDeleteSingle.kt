/* MediaDeleteSingle.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.MediaId
import io.ktor.client.call.body
import io.ktor.http.path

internal class MediaDeleteSingle(val file: MediaId) : BaseOperation<Unit>("Delete Single Media") {

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .get {
            url {
              path("gopro/media/delete/file")
              encodedParameters.append("path", file.asPath)
            }
          }
          .map { it.body() }
}
