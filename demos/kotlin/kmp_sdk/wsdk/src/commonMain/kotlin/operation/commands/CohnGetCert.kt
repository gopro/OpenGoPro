package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.exceptions.CameraInternalError
import entity.network.GpUuid
import entity.operation.CameraControlStatus
import extensions.isOk
import extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.http.path
import open_gopro.EnumCameraControlStatus
import open_gopro.RequestSetCameraControlStatus
import open_gopro.ResponseCOHNCert
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

class CohnGetCert :
    BaseOperation<String>("Get COHN Cert") {

    override suspend fun execute(communicator: BleCommunicator): Result<String> =
        communicator.executeProtobufCommand(
            FeatureId.QUERY,
            ActionId.REQUEST_GET_COHN_CERT,
            byteArrayOf(),
            ResponseId.Protobuf(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_CERT),
            GpUuid.CQ_QUERY
        ).fold(
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
            onFailure = { Result.failure(it) }
        )

    override suspend fun execute(communicator: HttpCommunicator): Result<String> =
        communicator.get { url { path("GoProRootCA.crt") } }.map { it.body() }
}



