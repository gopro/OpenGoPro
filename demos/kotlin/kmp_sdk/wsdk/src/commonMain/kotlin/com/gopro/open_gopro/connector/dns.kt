/* dns.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.connector

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.connector.IConnector
import com.gopro.open_gopro.domain.data.ICameraRepository
import com.gopro.open_gopro.domain.network.IDnsApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

internal class GpDnsConnector(
    private val dnsApi: IDnsApi,
    private val cameraRepo: ICameraRepository
) : IConnector<ScanResult.Dns, ConnectionDescriptor.Http> {
  // TODO how to choose USB / WIFI here? Does it even matter?
  override val networkType = NetworkType.WIFI_WLAN

  override suspend fun scan(): Result<Flow<ScanResult.Dns>> =
      dnsApi.scan(NSD_GP_SERVICE_TYPE).map { flow ->
        flow.map { scanResult ->
          ScanResult.Dns(
              GoProId(scanResult.serviceName.takeLast(4)),
              scanResult.ipAddress,
              NetworkType.WIFI_WLAN // TODO can we select between usb and wifi here?
              )
        }
      }

  override suspend fun connect(
      target: ScanResult.Dns,
      request: ConnectionRequestContext?
  ): Result<ConnectionDescriptor.Http> =
      cameraRepo.getHttpsCredentials(target.id).map { credentials ->
        ConnectionDescriptor.Http(
            id = target.id,
            ipAddress = target.ipAddress,
            port = null, // TODO can we get this?
            credentials = credentials)
      }

  override suspend fun disconnect(connection: ConnectionDescriptor.Http): Result<Unit> = TODO()

  companion object {
    const val NSD_GP_SERVICE_TYPE = "_gopro-web._tcp."
  }
}
