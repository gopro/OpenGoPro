/* LivestreamConfigure.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.EnumLens
import com.gopro.open_gopro.operations.EnumWindowSize
import com.gopro.open_gopro.operations.LivestreamConfigurationRequest
import com.gopro.open_gopro.operations.RequestSetLiveStreamMode
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.http.path
import pbandk.ByteArr
import pbandk.encodeToByteArray

internal class LivestreamConfigure(val request: LivestreamConfigurationRequest) :
    BaseOperation<Unit>("Configure Livestream") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> {
    val protoRequest =
        with(request) {
          RequestSetLiveStreamMode(
              url = url,
              encode = shouldEncode,
              windowSize = resolution?.let { EnumWindowSize.fromValue(it.value) },
              cert = certificate?.let { ByteArr(it) },
              minimumBitrate = minimumBitrate,
              maximumBitrate = maximumBitrate,
              startingBitrate = startingBitRate,
              lens = fov?.let { EnumLens.fromValue(it.value) })
        }
    return communicator
        .executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.SET_LIVESTREAM_MODE,
            protoRequest.encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.SET_LIVESTREAM_MODE_RSP),
            GpUuid.CQ_COMMAND)
        .mapFromGenericProtoResponseToResult()
  }

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .post {
            contentType(ContentType.Application.Json)
            url { path("gopro/livestream/setup") }
            setBody(request)
          }
          .map { it.body() }
}
