/* MediaGetLastCaptured.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.MediaId
import com.gopro.open_gopro.operations.RequestGetLastCapturedMedia
import com.gopro.open_gopro.operations.ResponseLastCapturedMedia
import com.gopro.open_gopro.util.extensions.isOk
import io.ktor.client.call.body
import io.ktor.http.path
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

internal class MediaGetLastCaptured : BaseOperation<MediaId>("Get Last Captured MediaId") {

  override suspend fun execute(communicator: BleCommunicator): Result<MediaId> =
      communicator
          .executeProtobufCommand(
              FeatureId.QUERY,
              ActionId.REQUEST_GET_LAST_MEDIA,
              RequestGetLastCapturedMedia().encodeToByteArray(),
              ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_LAST_MEDIA),
              GpUuid.CQ_COMMAND)
          .map {
            ResponseLastCapturedMedia.decodeFromByteArray(it).let { response ->
              if (response.result?.isOk() == true) {
                MediaId(
                    response.media?.file ?: throw CameraInternalError("Did not receive a file."),
                    response.media?.folder
                        ?: throw CameraInternalError("Did not receive a folder."))
              } else {
                throw CameraInternalError("Did not receive a result.")
              }
            }
          }

  override suspend fun execute(communicator: HttpCommunicator): Result<MediaId> =
      communicator.get { url { path("gopro/media/last_captured") } }.map { it.body() }
}
