/* SetPairingComplete.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Fri Jun  6 17:50:52 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.EnumPairingFinishState
import com.gopro.open_gopro.operations.RequestPairingFinish
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import pbandk.encodeToByteArray

internal class SetPairingComplete : BaseOperation<Unit>("Set Pairing Complete") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> {
    val request =
        RequestPairingFinish(result = EnumPairingFinishState.SUCCESS, phoneName = "phoneName")
    return communicator
        .executeProtobufCommand(
            FeatureId.WIRELESS_MANAGEMENT,
            ActionId.REQUEST_PAIRING_STATE,
            request.encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.WIRELESS_MANAGEMENT, ActionId.REQUEST_PAIRING_STATE_RSP),
            GpUuid.CM_NET_MGMT_COMM)
        .mapFromGenericProtoResponseToResult()
  }
}
