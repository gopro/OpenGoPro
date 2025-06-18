/* AccessPointFeature.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.ApScanEntry
import com.gopro.open_gopro.operations.isFinished
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.last
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.withTimeout

private val logger = Logger.withTag("AccessPointFeature")

private const val CONNECT_TIMEOUT_MS = 30000L

/**
 * Scan and connect the camera to an Access Point
 *
 * The camera operates in STA mode when connected to the Access Point
 *
 * @property context feature context
 * @see [STA mode](https://gopro.github.io/OpenGoPro/tutorials/connect-wifi#station-sta-mode)
 */
class AccessPointFeature internal constructor(private val context: IFeatureContext) {
  private val _state: MutableStateFlow<AccessPointState> =
      MutableStateFlow(AccessPointState.Disconnected)
  val state: StateFlow<AccessPointState>
    get() = _state

  private fun setState(newState: AccessPointState) {
    logger.d { "Setting access point state to $newState" }
    _state.update { newState }
  }

  /**
   * Scan for available Access Points
   *
   * @return list of discovered access points
   * @see
   *   [Open GoPro spec](https://gopro.github.io/OpenGoPro/ble/features/access_points.html#scan-for-access-points)
   */
  suspend fun scanForAccessPoints(): Result<List<ApScanEntry>> {
    logger.i("Scanning for access points")
    // First perform scan and store scan result
    return context.gopro.commands
        .scanAccessPoint()
        .fold(
            onFailure = {
              return Result.failure(it)
            },
            onSuccess = {
              logger.i("Retrieving access point scan results.")
              // Collect until completion and operate on the last response
              it.last().let { scanResult ->
                // Now return the actual results
                context.gopro.commands
                    .getAccessPointScanResults(
                        scanResult.scanId ?: throw Exception("Scan result did not contain ID"),
                        scanResult.totalEntries
                            ?: throw Exception("Scan result did not contain total entries"))
                    .onSuccess { results ->
                      logger.i("Received ${results.size} access point scan results")
                    }
              }
            })
  }

  private suspend fun processConnectFlowResult(
      ssid: String,
      result: Result<Flow<AccessPointState>>
  ): Result<Unit> =
      result.fold(
          onSuccess = { flow ->
            flow
                .onEach { setState(it) }
                .first { it.isFinished() }
                .let { finalState ->
                  when (finalState) {
                    is AccessPointState.Connected -> {
                      logger.i("Successfully connected to access point: $ssid")
                      Result.success(Unit)
                    }
                    else -> {
                      logger.w("Connection to $ssid failed")
                      Result.failure(Exception("Failed to connect to access point: $ssid"))
                    }
                  }
                }
          },
          onFailure = {
            logger.e("Failed to connect to access point: $ssid", it)
            Result.failure(it)
          })

  private suspend fun robustlyConnect(action: suspend () -> Result<Unit>): Result<Unit> {
    for (retry in 1..3) {
      runCatching {
            withTimeout(CONNECT_TIMEOUT_MS) {
              action().onFailure {
                // Re-raise for runCatching otherwise Failure would be swallowed
                throw Exception(it)
              }
            }
          }
          .onSuccess {
            return Result.success(Unit)
          }
          .onFailure {
            logger.w("Failed to connect on attempt $retry: ${it.message}")
            disconnectAccessPoint()
            scanForAccessPoints()
          }
    }
    return Result.failure(Exception("Failed to connect after 3 attempts"))
  }

  /**
   * Connect to a previously provisioned access point
   *
   * @param ssid target SSID to connect to
   * @return continuous connection states
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/access_points.html#connect-to-provisioned-access-point)
   */
  suspend fun connectAccessPoint(ssid: String): Result<Unit> {
    if (_state.value is AccessPointState.Connected) {
      "Already connected to an access point, must disconnect first."
          .let {
            logger.w(it)
            return Result.failure(Exception(it))
          }
    }
    logger.i("Connecting to $ssid")
    return robustlyConnect {
      processConnectFlowResult(ssid, context.gopro.commands.connectAccessPoint(ssid))
    }
  }

  /**
   * Connect to an access point that has not been previously provisioned
   *
   * @param ssid target SSID to connect to
   * @param password password for target SSID
   * @return continuous connection states
   */
  suspend fun connectAccessPoint(ssid: String, password: String): Result<Unit> {
    if (_state.value is AccessPointState.Connected) {
      "Already connected to an access point, must disconnect first."
          .let {
            logger.w(it)
            return Result.failure(Exception(it))
          }
    }
    logger.i("Connecting to $ssid with password ${"*".repeat(password.length)}")
    return robustlyConnect {
      processConnectFlowResult(ssid, context.gopro.commands.connectAccessPoint(ssid, password))
    }
  }

  /**
   * Disconnect from the currently connected access point
   *
   * @return result of the disconnect operation
   * @see
   *   [Open GoPro Spec](http://gopro.github.io/OpenGoPro/ble/features/access_points.html#disconnect-from-access-point)
   */
  suspend fun disconnectAccessPoint(): Result<Unit> {
    logger.i("Disconnecting from access point")
    return context.gopro.commands
        .setApMode(true)
        .onSuccess {
          setState(AccessPointState.Disconnected)
          logger.i("Disconnected from access point")
        }
        .onFailure { logger.e("Failed to disconnect from access point", it) }
  }
}
