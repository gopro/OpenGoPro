/* AccessPointScan.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.ApScanResult
import com.gopro.open_gopro.operations.EnumScanning
import com.gopro.open_gopro.operations.NotifStartScanning
import com.gopro.open_gopro.operations.ResponseStartScanning
import com.gopro.open_gopro.util.extensions.isOk
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.transformWhile
import pbandk.decodeFromByteArray

private val logger = Logger.withTag("Access Point Scan Operation")

private fun isScanningStateSuccess(scanState: EnumScanning): Boolean =
    when (scanState) {
      is EnumScanning.SCANNING_NEVER_STARTED,
      is EnumScanning.SCANNING_ABORTED_BY_SYSTEM,
      is EnumScanning.SCANNING_CANCELLED_BY_USER,
      is EnumScanning.SCANNING_SUCCESS -> false

      else -> true
    }

private fun isScanResultSuccess(scanResult: NotifStartScanning): Boolean =
    isScanningStateSuccess(scanResult.scanningState)

private fun isScanResultSuccess(scanResult: ResponseStartScanning): Boolean =
    isScanningStateSuccess(scanResult.scanningState) && scanResult.result.isOk()

internal class AccessPointScan : BaseOperation<Flow<ApScanResult>>("Scan for Access Points") {

  @OptIn(ExperimentalUnsignedTypes::class)
  override suspend fun execute(communicator: BleCommunicator): Result<Flow<ApScanResult>> {
    // First ensure the initial request is successful, returning in any fail case.
    communicator
        .executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.SCAN_WIFI_NETWORKS,
            byteArrayOf(),
            ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.SCAN_WIFI_NETWORKS_RSP),
            GpUuid.CM_NET_MGMT_COMM)
        .fold(
            onSuccess = {
              ResponseStartScanning.decodeFromByteArray(it).let { scanResult ->
                if (!isScanResultSuccess(scanResult)) {
                  return Result.failure(CameraInternalError("Received error status: $scanResult"))
                }
              }
            },
            onFailure = {
              return Result.failure(it)
            })

    // Now register with the BLE controller to receive updates
    return communicator
        .registerUpdate(
            ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.NOTIF_START_SCAN))
        // Map the raw protobuf response flow to the correct return type
        .map { flow ->
          flow
              .map { NotifStartScanning.decodeFromByteArray(it.payload.toByteArray()) }
              .transformWhile {
                // Note. CompleteAfter would be really nice here:
                // https://github.com/Kotlin/kotlinx.coroutines/issues/3299
                emit(it) // Always emit
                // Choose to continue based on scan state
                isScanResultSuccess(it)
              }
              .map { ApScanResult(it.scanId, it.totalEntries, it.totalConfiguredSsid) }
        }
  }
}
