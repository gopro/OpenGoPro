/* CohnGetCert.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
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
import com.gopro.open_gopro.operations.ResponseCOHNCert
import com.gopro.open_gopro.util.extensions.isOk
import io.ktor.client.call.body
import io.ktor.http.path
import pbandk.decodeFromByteArray

internal class CohnGetCert : BaseOperation<String>("Get COHN Cert") {

  override suspend fun execute(communicator: BleCommunicator): Result<String> =
      communicator
          .executeProtobufCommand(
              FeatureId.QUERY,
              ActionId.REQUEST_GET_COHN_CERT,
              byteArrayOf(),
              ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_CERT),
              GpUuid.CQ_QUERY)
          .fold(
              onSuccess = {
                ResponseCOHNCert.decodeFromByteArray(it).let { response ->
                  response.cert?.let { cert ->
                    if (response.result?.isOk() == true) {
                      Result.success(cert)
                    } else {
                      Result.failure(CameraInternalError("received non-success status"))
                    }
                  } ?: Result.failure(CameraInternalError("Did not receive cert"))
                }
              },
              onFailure = { Result.failure(it) })

  override suspend fun execute(communicator: HttpCommunicator): Result<String> =
      communicator.get { url { path("GoProRootCA.crt") } }.map { it.body() }
}
