package operation.commands

import entity.operation.CohnSettingRequest
import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.path
import open_gopro.RequestSetCOHNSetting
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
            url { path("gopro/cohn/setting") }
            setBody(CohnSettingRequest(!disableCohn))
        }.map { it.body() }
}