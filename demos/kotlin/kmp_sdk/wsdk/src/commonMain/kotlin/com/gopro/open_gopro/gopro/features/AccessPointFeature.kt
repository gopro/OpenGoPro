package com.gopro.open_gopro.gopro.features

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.entity.operation.AccessPointState
import com.gopro.open_gopro.entity.operation.ApScanEntry
import com.gopro.open_gopro.gopro.IFeatureContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.last
import kotlinx.coroutines.flow.onEach

private val logger = Logger.withTag("AccessPointFeature")

/**
 * Scan and connect the camera to an Access Point
 *
 * The camera operates in STA mode when connected to the Access Point
 *
 * @see [STA mode](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#station-sta-mode)
 *
 * @property context feature context
 */
class AccessPointFeature internal constructor(private val context: IFeatureContext) {
    /**
     * Scan for available Access Points
     *
     * @see [Open GoPro spec](https://gopro.github.io/OpenGoPro/ble/features/access_points.html#scan-for-access-points)
     *
     * @return list of discovered access points
     */
    suspend fun scanForAccessPoints(): Result<List<ApScanEntry>> {
        logger.i("Scanning for access points")
        // First perform scan and store scan result
        return context.gopro.commands.scanAccessPoint().fold(
            onFailure = { return Result.failure(it) },
            onSuccess = {
                logger.i("Retrieving access point scan results.")
                // Collect until completion and operate on the last response
                it.last().let { scanResult ->
                    // Now return the actual results
                    context.gopro.commands.getAccessPointScanResults(
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

    /**
     * Connect to a previously provisioned access point
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/access_points.html#connect-to-provisioned-access-point)
     *
     * @param ssid target SSID to connect to
     * @return continuous connection states
     */
    suspend fun connectAccessPoint(ssid: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid")
        return context.gopro.commands.connectAccessPoint(ssid).map { flow ->
            flow.onEach { context.gpDescriptorManager.setAccessPointState(it) }
        }
    }

    /**
     * Connect to an access point that has not been previously provisioned
     *
     * @param ssid target SSID to connect to
     * @param password password for target SSID
     * @return continuous connection states
     */
    suspend fun connectAccessPoint(ssid: String, password: String): Result<Flow<AccessPointState>> {
        logger.i("Connecting to $ssid with password ${"*".repeat(password.length)}")
        return context.gopro.commands.connectAccessPoint(ssid, password).map { flow ->
            flow.onEach {
                context.gpDescriptorManager.setAccessPointState(it)
            }
        }
    }
}