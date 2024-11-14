package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.ActionId
import entity.communicator.FeatureId
import entity.exceptions.CameraInternalError
import entity.network.GpUuid
import entity.operation.ApScanEntry
import entity.operation.proto.RequestGetApEntries
import entity.operation.proto.ResponseGetApEntries
import extensions.isOk
import extensions.toBoolean
import pbandk.decodeFromByteArray
import pbandk.encodeToByteArray

private const val IS_AUTH_MASK = 1.shl(0) // NOTE. Open is just inverse of this value.
private const val IS_CONF_MASK = 1.shl(1)
private const val IS_BEST_SSID_MASK = 1.shl(2)
private const val IS_ASSOC_MASK = 1.shl(3)

internal class AccessPointGetScanResults(val scanId: Int, val totalEntries: Int) :
    BaseOperation<List<ApScanEntry>>("Get AP Scan Results") {

    override suspend fun execute(communicator: BleCommunicator): Result<List<ApScanEntry>> =
        communicator.executeProtobufCommand(
            FeatureId.NETWORK_MANAGEMENT,
            ActionId.GET_AP_ENTRIES,
            RequestGetApEntries(0, totalEntries, scanId).encodeToByteArray(),
            ResponseId.Protobuf(
                FeatureId.NETWORK_MANAGEMENT,
                ActionId.GET_AP_ENTRIES_RSP
            ),
            GpUuid.CM_NET_MGMT_COMM
        ).map {
            ResponseGetApEntries.decodeFromByteArray(it).let { response ->
                if (response.result.isOk()) {
                    response.entries.map { entry ->
                        ApScanEntry(
                            ssid = entry.ssid,
                            signalStrengthBars = entry.signalStrengthBars,
                            signalFrequencyMhz = entry.signalFrequencyMhz,
                            isAuthenticated = entry.scanEntryFlags.and(IS_AUTH_MASK)
                                .toBoolean(),
                            isOpen = !entry.scanEntryFlags.and(IS_AUTH_MASK).toBoolean(),
                            isAssociated = entry.scanEntryFlags.and(IS_ASSOC_MASK)
                                .toBoolean(),
                            isConfigured = entry.scanEntryFlags.and(IS_CONF_MASK)
                                .toBoolean(),
                            isBestSsid = entry.scanEntryFlags.and(IS_BEST_SSID_MASK)
                                .toBoolean()
                        )
                    }
                } else {
                    throw CameraInternalError("Received error status: ${response.result}.")
                }
            }
        }

}
