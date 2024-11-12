package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.exceptions.CameraInternalError
import entity.network.GpUuid
import entity.operation.AccessPointState
import entity.operation.isFinished
import extensions.isOk
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.transformWhile
import open_gopro.EnumProvisioning
import open_gopro.NotifProvisioningState
import open_gopro.RequestConnect
import open_gopro.RequestConnectNew
import open_gopro.ResponseConnect
import open_gopro.ResponseConnectNew
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private fun EnumProvisioning.toConnectState(ssid: String): AccessPointState =
    when (this) {
        is EnumProvisioning.PROVISIONING_ABORTED_BY_SYSTEM,
        is EnumProvisioning.PROVISIONING_CANCELLED_BY_USER,
        is EnumProvisioning.PROVISIONING_ERROR_FAILED_TO_ASSOCIATE,
        is EnumProvisioning.PROVISIONING_ERROR_NO_INTERNET,
        is EnumProvisioning.PROVISIONING_ERROR_PASSWORD_AUTH,
        is EnumProvisioning.PROVISIONING_ERROR_UNSUPPORTED_TYPE,
        is EnumProvisioning.PROVISIONING_NEVER_STARTED,
        is EnumProvisioning.UNRECOGNIZED,
        is EnumProvisioning.PROVISIONING_UNKNOWN,
        is EnumProvisioning.PROVISIONING_ERROR_EULA_BLOCKING -> AccessPointState.Disconnected

        is EnumProvisioning.PROVISIONING_STARTED -> AccessPointState.InProgress(ssid)

        is EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP,
        is EnumProvisioning.PROVISIONING_SUCCESS_OLD_AP -> AccessPointState.Connected(ssid)
    }

@OptIn(ExperimentalUnsignedTypes::class)
private fun createConnectionFlow(
    ssid: String,
    communicator: BleCommunicator
): Result<Flow<AccessPointState>> =
    // Now register with the BLE controller to receive updates
    communicator.registerUpdate(
        ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.NOTIF_PROVIS_STATE)
    )
        // Map the raw protobuf response flow to the correct return type
        .map { flow ->
            flow
                .transformWhile {
                    NotifProvisioningState
                        .decodeFromByteArray(it.payload.toByteArray()).provisioningState
                        .toConnectState(ssid)
                        .let { connectState ->
                            emit(connectState) // Always emit first
                            !connectState.isFinished() // Choose to continue based on connect state
                        }
                }.onStart {
                    emit(AccessPointState.InProgress(ssid))
                }
        }

class ConnectNewAccessPoint(val ssid: String, val password: String) :
    BaseOperation<Flow<AccessPointState>>("Connect to New Access Point") {

    override suspend fun execute(communicator: BleCommunicator): Result<Flow<AccessPointState>> {
        // First ensure the initial request is successful, returning in any fail case.
        communicator.executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.REQUEST_WIFI_CONNECT_NEW,
            RequestConnectNew(ssid = ssid, password = password).encodeToByteArray(),
            ResponseId.Protobuf(
                FeatureId.NETWORK_MANAGEMENT,
                ActionId.REQUEST_WIFI_CONNECT_NEW_RSP
            ),
            GpUuid.CM_NET_MGMT_COMM
        ).fold(
            onSuccess = {
                ResponseConnectNew.decodeFromByteArray(it).let { response ->
                    if ((!response.result.isOk()) ||
                        (response.provisioningState.toConnectState(ssid) is AccessPointState.Disconnected)
                    ) {
                        return Result.failure(CameraInternalError("Received error status: $response"))
                    }
                }
            },
            onFailure = { return Result.failure(it) }
        )
        return createConnectionFlow(ssid, communicator)
    }
}

class ConnectProvisionedAccessPoint(val ssid: String) :
    BaseOperation<Flow<AccessPointState>>("Connect to Provisioned Access Point") {

    override suspend fun execute(communicator: BleCommunicator): Result<Flow<AccessPointState>> {
        // First ensure the initial request is successful, returning in any fail case.
        communicator.executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.REQUEST_WIFI_CONNECT,
            RequestConnect(ssid = ssid).encodeToByteArray(),
            ResponseId.Protobuf(
                FeatureId.NETWORK_MANAGEMENT,
                ActionId.REQUEST_WIFI_CONNECT_RSP
            ),
            GpUuid.CM_NET_MGMT_COMM
        ).fold(
            onSuccess = {
                ResponseConnect.decodeFromByteArray(it).let { response ->
                    if ((!response.result.isOk()) ||
                        (response.provisioningState.toConnectState(ssid) is AccessPointState.Disconnected)
                    ) {
                        return Result.failure(CameraInternalError("Received error status: $response"))
                    }
                }
            },
            onFailure = { return Result.failure(it) }
        )
        return createConnectionFlow(ssid, communicator)
    }
}