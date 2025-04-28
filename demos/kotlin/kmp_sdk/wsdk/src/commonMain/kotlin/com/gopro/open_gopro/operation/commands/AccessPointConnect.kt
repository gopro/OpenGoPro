/* AccessPointConnect.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.EnumProvisioning
import com.gopro.open_gopro.operations.NotifProvisioningState
import com.gopro.open_gopro.operations.RequestConnect
import com.gopro.open_gopro.operations.RequestConnectNew
import com.gopro.open_gopro.operations.ResponseConnect
import com.gopro.open_gopro.operations.ResponseConnectNew
import com.gopro.open_gopro.operations.isFinished
import com.gopro.open_gopro.util.extensions.isOk
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.transformWhile
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

      else -> throw Exception("Received unknown Enum Provision state: $this")
    }

@OptIn(ExperimentalUnsignedTypes::class)
private fun createConnectionFlow(
    ssid: String,
    communicator: BleCommunicator
): Result<Flow<AccessPointState>> =
    // Now register with the BLE controller to receive updates
    communicator
        .registerUpdate(
            ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.NOTIF_PROVIS_STATE))
        // Map the raw protobuf response flow to the correct return type
        .map { flow ->
          flow
              .transformWhile {
                NotifProvisioningState.decodeFromByteArray(it.payload.toByteArray())
                    .provisioningState
                    .toConnectState(ssid)
                    .let { connectState ->
                      emit(connectState) // Always emit first
                      !connectState.isFinished() // Choose to continue based on connect state
                    }
              }
              .onStart { emit(AccessPointState.InProgress(ssid)) }
        }

internal class ConnectNewAccessPoint(val ssid: String, val password: String) :
    BaseOperation<Flow<AccessPointState>>("Connect to New Access Point") {

  override suspend fun execute(communicator: BleCommunicator): Result<Flow<AccessPointState>> {
    // First ensure the initial request is successful, returning in any fail case.
    communicator
        .executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.REQUEST_WIFI_CONNECT_NEW,
            // Hard code bypass_eula_check to True.
            // On cameras where it is supported, the connection should succeed regardless of whether
            // or not there is internet access.
            // On cameras where it is not supported, it should be ignore
            RequestConnectNew(ssid = ssid, password = password, bypassEulaCheck = true)
                .encodeToByteArray(),
            ResponseId.Protobuf(
                FeatureId.NETWORK_MANAGEMENT, ActionId.REQUEST_WIFI_CONNECT_NEW_RSP),
            GpUuid.CM_NET_MGMT_COMM)
        .fold(
            onSuccess = {
              ResponseConnectNew.decodeFromByteArray(it).let { response ->
                if ((!response.result.isOk()) ||
                    (response.provisioningState.toConnectState(ssid)
                        is AccessPointState.Disconnected)) {
                  return Result.failure(CameraInternalError("Received error status: $response"))
                }
              }
            },
            onFailure = {
              return Result.failure(it)
            })
    return createConnectionFlow(ssid, communicator)
  }
}

internal class ConnectProvisionedAccessPoint(val ssid: String) :
    BaseOperation<Flow<AccessPointState>>("Connect to Provisioned Access Point") {

  override suspend fun execute(communicator: BleCommunicator): Result<Flow<AccessPointState>> {
    // First ensure the initial request is successful, returning in any fail case.
    communicator
        .executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.REQUEST_WIFI_CONNECT,
            RequestConnect(ssid = ssid).encodeToByteArray(),
            ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.REQUEST_WIFI_CONNECT_RSP),
            GpUuid.CM_NET_MGMT_COMM)
        .fold(
            onSuccess = {
              ResponseConnect.decodeFromByteArray(it).let { response ->
                if ((!response.result.isOk()) ||
                    (response.provisioningState.toConnectState(ssid)
                        is AccessPointState.Disconnected)) {
                  return Result.failure(CameraInternalError("Received error status: $response"))
                }
              }
            },
            onFailure = {
              return Result.failure(it)
            })
    return createConnectionFlow(ssid, communicator)
  }
}
