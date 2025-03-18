/* ble.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.connector

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.communicator.bleCommunicator.GpBleAdvertisement
import com.gopro.open_gopro.domain.connector.IConnector
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.entity.network.ble.BleAdvertisement
import com.gopro.open_gopro.entity.network.ble.GpUuid
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import org.koin.core.component.KoinComponent

private val notifiableUuids =
    listOf(
            GpUuid.CQ_COMMAND_RESP,
            GpUuid.CQ_QUERY_RESP,
            GpUuid.CQ_SETTINGS_RESP,
            GpUuid.CN_NET_MGMT_RESP)
        .map { it.toUuid() }
        .toSet()

internal class GpBleConnector(private val bleApi: IBleApi) :
    IConnector<ScanResult.Ble, ConnectionDescriptor.Ble>, KoinComponent {
  override val networkType = NetworkType.BLE

  private val idAdvMap = mutableMapOf<GoProId, BleAdvertisement>()

  override suspend fun scan(): Result<Flow<ScanResult.Ble>> =
      bleApi.scan(setOf(GpUuid.S_CONTROL_QUERY.toUuid())).map { flow ->
        flow
            .onStart { idAdvMap.clear() }
            .onEach { idAdvMap[GoProId(it.name!!.takeLast(4))] = it }
            .map {
              val serialNumber =
                  GpBleAdvertisement.Builder()
                      .name(it.name)
                      .serviceData(it.service?.get(GpUuid.S_CONTROL_QUERY.toUuid()))
                      .manufacturerData(it.manufacturerData)
                      .build()
                      .serialNumber
              ScanResult.Ble(GoProId(serialNumber.takeLast(4)), it.id, it.name ?: "")
            }
      }

  override suspend fun connect(
      target: ScanResult.Ble,
      request: ConnectionRequestContext?
  ): Result<ConnectionDescriptor.Ble> =
      bleApi
          .connect(idAdvMap.getValue(target.id))
          .fold(
              onFailure = {
                return Result.failure(it)
              },
              onSuccess = { device ->
                bleApi.enableNotifications(device, notifiableUuids).map {
                  ConnectionDescriptor.Ble(target.id, device)
                }
              })

  override suspend fun disconnect(connection: ConnectionDescriptor.Ble): Result<Unit> =
      bleApi.disconnect(connection.device)
}
