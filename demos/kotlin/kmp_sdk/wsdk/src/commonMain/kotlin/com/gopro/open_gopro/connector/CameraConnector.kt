/* CameraConnector.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.connector

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.connector.IConnector
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.merge
import org.koin.core.component.KoinComponent

internal class CameraConnector
internal constructor(
    private val bleConnector: IConnector<ScanResult.Ble, ConnectionDescriptor.Ble>,
    private val wifiConnector: IConnector<ScanResult.Wifi, ConnectionDescriptor.Http>,
    private val dnsConnector: IConnector<ScanResult.Dns, ConnectionDescriptor.Http>,
) : ICameraConnector, KoinComponent {
  override suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> =
      networkTypes
          .map { networkType ->
            when (networkType) {
                  NetworkType.BLE -> bleConnector
                  NetworkType.WIFI_WLAN -> dnsConnector
                  NetworkType.WIFI_AP -> wifiConnector
                  NetworkType.USB -> dnsConnector
                }
                .scan()
                .fold(onSuccess = { it }, onFailure = { throw Exception(it) })
          }
          .merge()

  override suspend fun connect(
      target: ScanResult,
      connectionRequestContext: ConnectionRequestContext?
  ): Result<ConnectionDescriptor> =
      when (target) {
        is ScanResult.Ble -> bleConnector.connect(target, connectionRequestContext)
        is ScanResult.Dns -> dnsConnector.connect(target, connectionRequestContext)
        is ScanResult.Wifi -> wifiConnector.connect(target, connectionRequestContext)
      }
}
