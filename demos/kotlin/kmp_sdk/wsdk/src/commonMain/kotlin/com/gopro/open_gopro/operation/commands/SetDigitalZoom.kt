/* SetDigitalZoom.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import io.ktor.client.call.body
import io.ktor.http.path

internal class SetDigitalZoom(val zoom: Int) : BaseOperation<Unit>("Set Digital Zoom") {

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .get {
            url {
              path("gopro/camera/digital_zoom")
              parameters.append("percent", zoom.toString())
            }
          }
          .map { it.body() }
}
