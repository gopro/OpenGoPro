/* AndroidDnsApi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.connector

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import co.touchlab.kermit.Logger
import com.gopro.open_gopro.domain.network.DnsScanResult
import com.gopro.open_gopro.domain.network.IDnsApi
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch

private val logger = Logger.withTag("AndroidDnsApi")

internal class AndroidDnsApi(context: Context, dispatcher: CoroutineDispatcher) : IDnsApi {
  private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
    logger.e("Caught exception in coroutine:", throwable)
  }

  private val scope = CoroutineScope(dispatcher + coroutineExceptionHandler)

  private val nsdManager: NsdManager = (context.getSystemService(Context.NSD_SERVICE) as NsdManager)

  private val mdnsScanResults = MutableSharedFlow<NsdServiceInfo>(replay = 10)

  private val nsdResolveListener =
      object : NsdManager.ResolveListener {
        override fun onServiceResolved(nsdServiceInfo: NsdServiceInfo) {
          logger.d("Resolve Succeeded: $nsdServiceInfo")
          scope.launch { mdnsScanResults.emit(nsdServiceInfo) }
        }

        override fun onResolveFailed(nsdServiceInfo: NsdServiceInfo, errorCode: Int) {
          logger.d("Resolve Failed: $nsdServiceInfo, errorCode: $errorCode")
        }
      }

  override suspend fun scan(serviceType: String): Result<Flow<DnsScanResult>> {
    val discoveryListener = DiscoveryListener(serviceType, nsdManager, nsdResolveListener)

    nsdManager.discoverServices(serviceType, NsdManager.PROTOCOL_DNS_SD, discoveryListener)
    return Result.success(
        mdnsScanResults
            .filter { it.hostAddresses.first().hostAddress != null }
            .map { DnsScanResult(it.hostAddresses.first().hostAddress!!, it.serviceName) })
  }

  private class DiscoveryListener(
      private val serviceType: String,
      private val nsdManager: NsdManager,
      private val nsdResolveListener: NsdManager.ResolveListener
  ) : NsdManager.DiscoveryListener {
    // TODO notify listeners?

    override fun onDiscoveryStarted(serviceType: String) {
      logger.d("Service discovery started: $serviceType")
    }

    override fun onDiscoveryStopped(serviceType: String) {
      logger.i("Discovery stopped: $serviceType")
    }

    override fun onStartDiscoveryFailed(serviceType: String, errorCode: Int) {
      logger.e("Start Discovery failed: Error code:$errorCode")
      nsdManager.stopServiceDiscovery(this)
    }

    override fun onStopDiscoveryFailed(serviceType: String, errorCode: Int) {
      logger.e("Stop Discovery failed: Error code:$errorCode")
      nsdManager.stopServiceDiscovery(this)
    }

    override fun onServiceLost(nsdServiceInfo: NsdServiceInfo) {
      // When the network service is no longer available.
      // Internal bookkeeping code goes here.
      // TODO does this need to be propagated to UI?
      logger.e("Service lost: $nsdServiceInfo")
    }

    override fun onServiceFound(nsdServiceInfo: NsdServiceInfo) {
      logger.d("Service discovery success: $nsdServiceInfo")
      if (nsdServiceInfo.serviceType != serviceType) {
        // Service type is the string containing the protocol and
        // transport layer for this service.
        logger.w("Unknown Service Type: ${nsdServiceInfo.serviceType}")
        return
      }
      onServiceDiscovered(nsdServiceInfo)
    }

    private fun onServiceDiscovered(nsdServiceInfo: NsdServiceInfo) {
      // TODO
      // Once a mDNS service it is discovered, it will take up to a minute to be "gone" after the
      // camera
      // turns off and/or camera goes disconnected from the Home Network. To assure the mDNS service
      // still
      // valid, we will "resolve" the service and send it back to app as result.
      logger.d("Service to resolve: ${nsdServiceInfo.serviceName}")
      nsdManager.resolveService(nsdServiceInfo, nsdResolveListener)
    }
  }
}
