/* CohnCreateCert.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.RequestCreateCOHNCert
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import pbandk.encodeToByteArray

internal class CohnCreateCert(val override: Boolean) : BaseOperation<Unit>("Create COHN Cert") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator
          .executeProtobufCommand(
              FeatureId.COMMAND,
              ActionId.REQUEST_CREATE_COHN_CERT,
              RequestCreateCOHNCert(override).encodeToByteArray(),
              ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_CREATE_COHN_CERT),
              GpUuid.CQ_COMMAND)
          .mapFromGenericProtoResponseToResult()
}
