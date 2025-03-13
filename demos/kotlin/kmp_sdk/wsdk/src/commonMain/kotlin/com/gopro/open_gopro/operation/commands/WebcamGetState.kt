/* WebcamGetState.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.operations.WebcamState
import io.ktor.client.call.body
import io.ktor.http.path

internal class WebcamGetState : BaseOperation<WebcamState>("Get Webcam Status") {

  override suspend fun execute(communicator: HttpCommunicator): Result<WebcamState> =
      communicator.get { url { path("gopro/webcam/status") } }.map { it.body() }
}
