package features

import co.touchlab.kermit.Logger
import entity.operation.AccessPointState
import entity.operation.ApScanEntry
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.last
import kotlinx.coroutines.flow.onEach
import operation.commands.AccessPointGetScanResults
import operation.commands.AccessPointScan
import operation.commands.ConnectNewAccessPoint
import operation.commands.ConnectProvisionedAccessPoint

private val logger = Logger.withTag("AccessPointFeature")

class AccessPointFeature(feature: FeatureContext) : IFeatureContext by feature {
    suspend fun scanForAccessPoints(): Result<List<ApScanEntry>> {
        logger.i("Scanning for access points")
        // First perform scan and store scan result
        return marshaller.marshal(AccessPointScan()).fold(
            onFailure = { return Result.failure(it) },
            onSuccess = {
                logger.i("Retrieving access point scan results.")
                // Collect until completion and operate on the last response
                it.last().let { scanResult ->
                    // Now return the actual results
                    marshaller.marshal(
                        AccessPointGetScanResults(
                            scanResult.scanId
                                ?: throw Exception("Scan result did not contain ID"),
                            scanResult.totalEntries
                                ?: throw Exception("Scan result did not contain total entries")
                        )
                    ).onSuccess { results ->
                        logger.i("Received ${results.size} access point scan results")
                    }
                }
            }
        )
    }

    suspend fun connectAccessPoint(ssid: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid")
        return marshaller.marshal(ConnectProvisionedAccessPoint(ssid)).map { flow ->
            flow.onEach { gpDescriptorManager.setAccessPointState(it) }
        }
    }

    suspend fun connectAccessPoint(ssid: String, password: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid with password ${"*".repeat(password.length)}")
        return marshaller.marshal(ConnectNewAccessPoint(ssid, password)).map { flow ->
            flow.onEach {
                gpDescriptorManager.setAccessPointState(it)
            }
        }
    }
}