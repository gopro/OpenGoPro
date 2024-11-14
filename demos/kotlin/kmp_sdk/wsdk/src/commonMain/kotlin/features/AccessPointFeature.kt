package features

import co.touchlab.kermit.Logger
import entity.operation.AccessPointState
import entity.operation.ApScanEntry
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.last
import kotlinx.coroutines.flow.onEach

private val logger = Logger.withTag("AccessPointFeature")

class AccessPointFeature internal constructor(feature: IFeatureContext) :
    IFeatureContext by feature {
    suspend fun scanForAccessPoints(): Result<List<ApScanEntry>> {
        logger.i("Scanning for access points")
        // First perform scan and store scan result
        return gopro.commands.scanAccessPoint().fold(
            onFailure = { return Result.failure(it) },
            onSuccess = {
                logger.i("Retrieving access point scan results.")
                // Collect until completion and operate on the last response
                it.last().let { scanResult ->
                    // Now return the actual results
                    gopro.commands.getAccessPointScanResults(
                        scanResult.scanId
                            ?: throw Exception("Scan result did not contain ID"),
                        scanResult.totalEntries
                            ?: throw Exception("Scan result did not contain total entries")
                    ).onSuccess { results ->
                        logger.i("Received ${results.size} access point scan results")
                    }
                }
            }
        )
    }

    suspend fun connectAccessPoint(ssid: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid")
        return gopro.commands.connectAccessPoint(ssid).map { flow ->
            flow.onEach { gpDescriptorManager.setAccessPointState(it) }
        }
    }

    suspend fun connectAccessPoint(ssid: String, password: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid with password ${"*".repeat(password.length)}")
        return gopro.commands.connectAccessPoint(ssid, password).map { flow ->
            flow.onEach {
                gpDescriptorManager.setAccessPointState(it)
            }
        }
    }
}