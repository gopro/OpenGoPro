package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.operations.CohnSettingRequest
import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.path
import com.gopro.open_gopro.operations.RequestSetCOHNSetting
import pbandk.encodeToByteArray

internal class CohnSetSetting(val disableCohn: Boolean) :
    BaseOperation<Unit>("Set COHN Setting") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
        communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.REQUEST_COHN_SETTING,
            // TODO I'm not sure this is correct. Its confusingly named.
            RequestSetCOHNSetting(cohnActive = !disableCohn).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_COHN_SETTING),
            GpUuid.CQ_COMMAND
        ).map { }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.post {
            url { path("com/gopro/open_gopro/gopro/cohn/setting") }
            setBody(CohnSettingRequest(!disableCohn))
        }.map { it.body() }
}