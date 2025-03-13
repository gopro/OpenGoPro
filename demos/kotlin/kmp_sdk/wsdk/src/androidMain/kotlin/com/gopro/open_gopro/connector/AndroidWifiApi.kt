/* AndroidWifiApi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.connector

import android.annotation.SuppressLint
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiManager
import android.net.wifi.WifiNetworkSpecifier
import android.provider.Settings
import co.touchlab.kermit.Logger
import com.gopro.open_gopro.domain.network.IWifiApi
import kotlin.time.DurationUnit
import kotlin.time.toDuration
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.timeout
import kotlinx.coroutines.launch

private val logger = Logger.withTag("AndroidWifiApi")

internal class AndroidWifiApi(
    private val context: Context,
    private val wifiManager: WifiManager,
    override val dispatcher: CoroutineDispatcher,
) : IWifiApi {
  private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
    logger.e("Caught exception in coroutine:", throwable)
  }

  private val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

  private val disconnects = MutableSharedFlow<String>(0)

  private val connectivityManager =
      context.applicationContext.getSystemService(Context.CONNECTIVITY_SERVICE)
          as ConnectivityManager

  private fun enableAdapter() {
    val panelIntent = Intent(Settings.Panel.ACTION_INTERNET_CONNECTIVITY)
    panelIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    context.startActivity(panelIntent)
  }

  override suspend fun setup() {
    if (!wifiManager.isWifiEnabled) enableAdapter()
  }

  // https://developer.android.com/develop/connectivity/wifi/wifi-scan
  override suspend fun scanForSsid(): Result<Flow<String>> {
    val flow =
        callbackFlow<String> {
          val wifiScanReceiver =
              object : BroadcastReceiver() {
                @SuppressLint("MissingPermission")
                override fun onReceive(context: Context, intent: Intent) {
                  val success = intent.getBooleanExtra(WifiManager.EXTRA_RESULTS_UPDATED, false)
                  if (success) {
                    wifiManager.scanResults.forEach { scanResult ->
                      logger.d("Discovered Wifi SSID ${scanResult.SSID}")
                      trySend(scanResult.SSID)
                    }
                  } else {
                    // TODO propagate error
                    logger.e("Wifi Scan failed")
                  }
                }
              }

          val intentFilter = IntentFilter()
          intentFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)
          context.registerReceiver(wifiScanReceiver, intentFilter)
          // TODO why is this (and start scan deprecated?
          logger.d("Starting Wifi SSID scan")
          if (!wifiManager.startScan()) logger.e("Failed to start wifi scan")
          awaitClose {
            context.unregisterReceiver(wifiScanReceiver)
            logger.d("Wifi SSID scan stopped.")
          }
        }
    return Result.success(flow)
  }

  @OptIn(FlowPreview::class)
  override suspend fun connect(ssid: String, password: String): Result<Unit> {
    val wifiNetworkSpecifier =
        WifiNetworkSpecifier.Builder().setSsid(ssid).setWpa2Passphrase(password).build()

    val networkRequest =
        NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .setNetworkSpecifier(wifiNetworkSpecifier)
            .build()

    logger.i("Connecting to Wifi AP: $ssid...")
    return callbackFlow {
          val callback =
              object : ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: Network) {
                  super.onAvailable(network)
                  // Note!! this prevents us from using LTE / the internet
                  if (connectivityManager.bindProcessToNetwork(network)) {
                    logger.i("Wifi connected")
                    trySend(Result.success(Unit))
                  } else {
                    logger.e("Wifi connection failed")
                    trySend(Result.failure(Exception("Wifi Connection failed")))
                  }
                }

                override fun onLost(network: Network) {
                  logger.e("Lost Wifi connection: $network")
                  scope.launch {
                    disconnects.emit(network.toString()) // TODO is this correct way to get ssid?
                  }
                  super.onLost(network)
                  connectivityManager.bindProcessToNetwork(null)
                  connectivityManager.unregisterNetworkCallback(this)
                }
              }
          connectivityManager.requestNetwork(networkRequest, callback)
          awaitClose { logger.d("Wifi connection request finished.") }
        }
        .timeout(CONNECTION_TIMEOUT)
        .catch { exception ->
          if (exception is TimeoutCancellationException) {
            "Wifi connect failed due to timeout of $CONNECTION_TIMEOUT"
                .let {
                  logger.e(it)
                  emit(Result.failure(Exception(it)))
                }
          } else {
            logger.e("Wifi connect failed due to unexpected ${exception.message}")
          }
        }
        .onEach { it.onFailure { error -> logger.e("$error") } }
        .first()
  }

  override suspend fun disconnect(ssid: String): Result<Unit> {
    TODO("Not yet implemented")
  }

  override fun receiveDisconnects(): Flow<String> = disconnects

  companion object {
    val CONNECTION_TIMEOUT = 30.toDuration(DurationUnit.SECONDS)
  }
}
