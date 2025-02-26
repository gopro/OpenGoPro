/* LivestreamGetStatus.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
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
import com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus
import com.gopro.open_gopro.operations.LivestreamError
import com.gopro.open_gopro.operations.LivestreamFov
import com.gopro.open_gopro.operations.LivestreamResolution
import com.gopro.open_gopro.operations.LivestreamState
import com.gopro.open_gopro.operations.LivestreamStatus
import com.gopro.open_gopro.operations.NotifyLiveStreamStatus
import com.gopro.open_gopro.operations.RequestGetLiveStreamStatus
import com.gopro.open_gopro.operations.isOk
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onCompletion
import kotlinx.coroutines.flow.onStart
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private fun NotifyLiveStreamStatus.toLivestreamStatus(): LivestreamStatus =
    LivestreamStatus(
        status = LivestreamState.fromValue(this.liveStreamStatus?.value),
        error = LivestreamError.fromValue(this.liveStreamError?.value),
        isEncodingSupported = this.liveStreamEncodeSupported,
        isMaxLensSupported = this.liveStreamMaxLensUnsupported?.not(),
        bitRate = this.liveStreamBitrate,
        maxBitrate = this.liveStreamMaximumStreamBitrate,
        minBitrate = this.liveStreamMinimumStreamBitrate,
        isEncoding = this.liveStreamEncode,
        isLensSupported = this.liveStreamLensSupported,
        supportedResolution =
            this.liveStreamWindowSizeSupportedArray.map {
              LivestreamResolution.fromValue(it.value)
            },
        supportedFov = this.liveStreamLensSupportedArray.map { LivestreamFov.fromValue(it.value) },
        isProtuneSupported = this.liveStreamProtuneSupported)

internal class LivestreamGetStatus :
    BaseOperation<Flow<LivestreamStatus>>("Get Livestream Status") {

  @OptIn(ExperimentalUnsignedTypes::class)
  override suspend fun execute(communicator: BleCommunicator): Result<Flow<LivestreamStatus>> {
    lateinit var initialStatus: LivestreamStatus
    // First ensure the initial request is successful, returning in any fail case.
    communicator
        .executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.GET_LIVESTREAM_STATUS,
            RequestGetLiveStreamStatus(
                    registerLiveStreamStatus =
                        listOf(EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS))
                .encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.LIVESTREAM_STATUS_RSP),
            GpUuid.CQ_QUERY)
        .fold(
            onSuccess = {
              initialStatus = NotifyLiveStreamStatus.decodeFromByteArray(it).toLivestreamStatus()
              initialStatus.let { status ->
                if (!status.isOk()) {
                  return Result.failure(CameraInternalError("Received error status: $status"))
                }
              }
            },
            onFailure = {
              return Result.failure(it)
            })

    // Now register with the BLE controller to receive updates
    return communicator
        .registerUpdate(ResponseId.Protobuf(FeatureId.QUERY, ActionId.LIVESTREAM_STATUS_NOTIF))
        .map { flow ->
          flow
              // Map the raw protobuf response flow to the correct return type
              .map {
                NotifyLiveStreamStatus.decodeFromByteArray(it.payload.toByteArray())
                    .toLivestreamStatus()
              }
              .onStart { emit(initialStatus) }
              .onCompletion {
                // Unregister on flow completion
                communicator.executeProtobufCommand(
                    FeatureId.QUERY,
                    ActionId.GET_LIVESTREAM_STATUS,
                    RequestGetLiveStreamStatus(
                            unregisterLiveStreamStatus =
                                listOf(
                                    EnumRegisterLiveStreamStatus
                                        .REGISTER_LIVE_STREAM_STATUS_STATUS))
                        .encodeToByteArray(),
                    ResponseId.Protobuf(FeatureId.QUERY, ActionId.LIVESTREAM_STATUS_RSP),
                    GpUuid.CQ_QUERY)
              }
        }
  }

  override suspend fun execute(communicator: HttpCommunicator): Result<Flow<LivestreamStatus>> =
      communicator.get { url { path("gopro/livestream/setup") } }.map { flow { emit(it.body()) } }
}
