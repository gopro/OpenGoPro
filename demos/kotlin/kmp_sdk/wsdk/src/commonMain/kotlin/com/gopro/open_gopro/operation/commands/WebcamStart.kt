/* WebcamStart.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.WebcamFov
import com.gopro.open_gopro.operations.WebcamProtocol
import com.gopro.open_gopro.operations.WebcamResolution
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamStart(
    val resolution: WebcamResolution? = null,
    val fov: WebcamFov? = null,
    val port: Int? = null,
    val protocol: WebcamProtocol? = null
) : BaseOperation<Unit>("Start Webcam") {

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .get {
            url {
              path("gopro/webcam/start")
              resolution?.let { parameters.append("res", it.value.toString()) }
              fov?.let { parameters.append("fov", it.value.toString()) }
              this@WebcamStart.port?.let { parameters.append("port", it.toString()) }
              this@WebcamStart.protocol?.let { parameters.append("protocol", it.value) }
            }
          }
          .map { it.body() }
}
