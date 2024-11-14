package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import exceptions.CameraInternalError
import entity.operation.MediaId
import entity.network.GpUuid
import extensions.isOk
import io.ktor.client.call.body
import io.ktor.http.path
import entity.operation.proto.RequestGetLastCapturedMedia
import entity.operation.proto.ResponseLastCapturedMedia
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

internal class MediaGetLastCaptured : BaseOperation<MediaId>("Get Last Captured MediaId") {

    override suspend fun execute(communicator: BleCommunicator): Result<MediaId> =
        communicator.executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.REQUEST_GET_LAST_MEDIA,
            RequestGetLastCapturedMedia().encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_LAST_MEDIA),
            GpUuid.CQ_COMMAND
        ).map {
            ResponseLastCapturedMedia.decodeFromByteArray(it).let { response ->
                if (response.result?.isOk() == true) {
                    MediaId(
                        response.media?.file
                            ?: throw CameraInternalError("Did not receive a file."),
                        response.media?.folder
                            ?: throw CameraInternalError("Did not receive a folder.")
                    )

                } else {
                    throw CameraInternalError("Did not receive a result.")
                }
            }
        }

    override suspend fun execute(communicator: HttpCommunicator): Result<MediaId> =
        communicator.get { url { path("gopro/media/last_captured") } }.map { it.body() }
}
