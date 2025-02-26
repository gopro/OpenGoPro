/* AccessPointGetScanResults.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.ApScanEntry
import com.gopro.open_gopro.operations.RequestGetApEntries
import com.gopro.open_gopro.operations.ResponseGetApEntries
import com.gopro.open_gopro.util.extensions.isOk
import com.gopro.open_gopro.util.extensions.toBoolean
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private const val IS_AUTH_MASK = 1.shl(0) // NOTE. Open is just inverse of this value.
private const val IS_CONF_MASK = 1.shl(1)
private const val IS_BEST_SSID_MASK = 1.shl(2)
private const val IS_ASSOC_MASK = 1.shl(3)

internal class AccessPointGetScanResults(val scanId: Int, val totalEntries: Int) :
    BaseOperation<List<ApScanEntry>>("Get AP Scan Results") {

  override suspend fun execute(communicator: BleCommunicator): Result<List<ApScanEntry>> =
      communicator
          .executeProtobufCommand(
              FeatureId.NETWORK_MANAGEMENT,
              ActionId.GET_AP_ENTRIES,
              RequestGetApEntries(0, totalEntries, scanId).encodeToByteArray(),
              ResponseId.Protobuf(FeatureId.NETWORK_MANAGEMENT, ActionId.GET_AP_ENTRIES_RSP),
              GpUuid.CM_NET_MGMT_COMM)
          .map {
            ResponseGetApEntries.decodeFromByteArray(it).let { response ->
              if (response.result.isOk()) {
                response.entries.map { entry ->
                  ApScanEntry(
                      ssid = entry.ssid,
                      signalStrengthBars = entry.signalStrengthBars,
                      signalFrequencyMhz = entry.signalFrequencyMhz,
                      isAuthenticated = entry.scanEntryFlags.and(IS_AUTH_MASK).toBoolean(),
                      isOpen = !entry.scanEntryFlags.and(IS_AUTH_MASK).toBoolean(),
                      isAssociated = entry.scanEntryFlags.and(IS_ASSOC_MASK).toBoolean(),
                      isConfigured = entry.scanEntryFlags.and(IS_CONF_MASK).toBoolean(),
                      isBestSsid = entry.scanEntryFlags.and(IS_BEST_SSID_MASK).toBoolean())
                }
              } else {
                throw CameraInternalError("Received error status: ${response.result}.")
              }
            }
          }
}
