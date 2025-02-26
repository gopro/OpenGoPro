/* wifi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.connector

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.connector.IConnector
import com.gopro.open_gopro.domain.network.IWifiApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

internal class GpWifiConnector(private val wifiApi: IWifiApi) :
    IConnector<ScanResult.Wifi, ConnectionDescriptor.Http> {
  override val networkType = NetworkType.WIFI_AP

  override suspend fun scan(): Result<Flow<ScanResult.Wifi>> =
      wifiApi.scanForSsid().map { it.map { id -> ScanResult.Wifi(GoProId(id), "NAME_TODO") } }

  override suspend fun connect(
      target: ScanResult.Wifi,
      request: ConnectionRequestContext?
  ): Result<ConnectionDescriptor.Http> =
      when (request) {
        is ConnectionRequestContext.Wifi ->
            wifiApi.connect(target.ssid, request.password).map {
              // The only Wifi AP use case is direct to camera so ip address and port are hardcoded.
              ConnectionDescriptor.Http(
                  ipAddress = GP_WIFI_AP_IP_ADDRESS, port = GP_WIFI_AP_PORT, id = target.id)
            }

        else -> throw Exception("Wifi connect requires password")
      }

  override suspend fun disconnect(connection: ConnectionDescriptor.Http): Result<Unit> = TODO()

  companion object {
    const val GP_WIFI_AP_IP_ADDRESS = "10.5.5.9"
    const val GP_WIFI_AP_PORT = 8080
  }
}
