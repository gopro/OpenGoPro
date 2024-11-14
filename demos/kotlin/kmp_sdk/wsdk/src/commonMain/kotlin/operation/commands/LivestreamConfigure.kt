package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.network.GpUuid
import entity.operation.LivestreamConfigurationRequest
import extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.http.path
import entity.operation.proto.EnumLens
import entity.operation.proto.EnumWindowSize
import entity.operation.proto.RequestSetLiveStreamMode
import pbandk.ByteArr
import pbandk.encodeToByteArray

internal class LivestreamConfigure(val request: LivestreamConfigurationRequest) :
    BaseOperation<Unit>("Configure Livestream") {

    override suspend fun execute(communicator: BleCommunicator): Result<Unit> {
        val protoRequest = with(request) {
            RequestSetLiveStreamMode(
                url = url,
                encode = shouldEncode,
                windowSize = resolution?.let { EnumWindowSize.fromValue(it.value) },
                cert = certificate?.let { ByteArr(it) },
                minimumBitrate = minimumBitrate,
                maximumBitrate = maximumBitrate,
                startingBitrate = startingBitRate,
                lens = fov?.let { EnumLens.fromValue(it.value) }
            )
        }
        return communicator.executeProtobufCommand(
            FeatureId.COMMAND,
            ActionId.SET_LIVESTREAM_MODE,
            protoRequest.encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.COMMAND, ActionId.SET_LIVESTREAM_MODE_RSP),
            GpUuid.CQ_COMMAND
        ).mapFromGenericProtoResponseToResult()
    }

    override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
        communicator.post {
            contentType(ContentType.Application.Json)
            url { path("gopro/livestream/setup") }
            setBody(request)
        }.map { it.body() }
}
