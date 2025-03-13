/* CohnGetStatus.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.CohnStatus
import com.gopro.open_gopro.operations.NotifyCOHNStatus
import com.gopro.open_gopro.operations.RequestGetCOHNStatus
import io.ktor.client.call.body
import io.ktor.http.path
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private fun NotifyCOHNStatus.toCohnStatus(): CohnStatus =
    CohnStatus(
        status = this.status,
        ssid = this.ssid,
        state = this.state,
        password = this.password,
        username = this.username,
        ipAddress = this.ipaddress,
        macAddress = this.macaddress,
        isEnabled = this.enabled)

internal class CohnGetStatus : BaseOperation<Flow<CohnStatus>>("Get COHN Status") {

  @OptIn(ExperimentalUnsignedTypes::class)
  override suspend fun execute(communicator: BleCommunicator): Result<Flow<CohnStatus>> {
    lateinit var initialStatue: NotifyCOHNStatus
    // First send the register command over the air
    communicator
        .executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.REQUEST_GET_COHN_STATUS,
            RequestGetCOHNStatus(true).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_STATUS),
            GpUuid.CQ_QUERY)
        .fold(
            onSuccess = {
              initialStatue =
                  NotifyCOHNStatus.decodeFromByteArray(it).also {
                    // TODO check error status here. I'm not sure which one we want.
                  }
            },
            onFailure = {
              return Result.failure(it)
            })

    // Now register to receive notifications
    return communicator
        .registerUpdate(
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_STATUS),
        )
        .map { flow ->
          flow
              .map { NotifyCOHNStatus.decodeFromByteArray(it.payload.toByteArray()).toCohnStatus() }
              .onStart { emit(initialStatue.toCohnStatus()) }
        }
  }

  override suspend fun execute(communicator: HttpCommunicator): Result<Flow<CohnStatus>> =
      communicator.get { url { path("GoProRootCA.crt") } }.map { it.body() }
}
