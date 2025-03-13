/* GoProFacadeFactory.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.DeviceNotFound
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.ICommunicator
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.domain.network.IHttpApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.domain.network.IWifiApi
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.util.GpCommonBase
import com.gopro.open_gopro.util.IGpCommonBase
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.launch

internal class GoProFactory(
    private val bleApi: IBleApi,
    private val httpApi: IHttpApi,
    private val wifiApi: IWifiApi,
    private val httpClientProvider: IHttpClientProvider,
    private val dispatcher: CoroutineDispatcher
) : IGoProFactory, IGpCommonBase by GpCommonBase("GoProFactory", dispatcher) {
  private val facadesById = mutableMapOf<GoProId, GoPro>()
  private val communicatorsByConnection = mutableMapOf<ConnectionDescriptor, ICommunicator<*>>()

  private fun httpCommunicatorsFromSsid(ssid: String): List<HttpCommunicator> =
      communicatorsByConnection
          .filterKeys { connection ->
            when (connection) {
              is ConnectionDescriptor.Ble -> false
              is ConnectionDescriptor.Http -> connection.ssid == ssid
            }
          }
          .values
          .map { it as HttpCommunicator }

  private fun bleCommunicatorsFromDevice(device: BleDevice): List<BleCommunicator> =
      communicatorsByConnection
          .filterKeys { connection ->
            when (connection) {
              is ConnectionDescriptor.Ble -> connection.device == device
              is ConnectionDescriptor.Http -> false
            }
          }
          .values
          .map { it as BleCommunicator }

  private suspend fun monitorBleConnections() =
      bleApi.receiveDisconnects().collect { device ->
        logger.d("Propagating BLE Disconnect from GoPro ${device.id}")
        // Find affected communicators (those whose BLE Device match the disconnected device)
        bleCommunicatorsFromDevice(device).forEach { communicator ->
          // Remove the affected communicator from any facade which uses it as a communicator
          facadesById.values.forEach { it.unbindCommunicator(communicator) }
        }
        // TODO reconnect

      }

  private suspend fun monitorWifiConnections() =
      wifiApi.receiveDisconnects().collect { ssid ->
        logger.d("Propagating Wifi Disconnect on $ssid")
        // Find affected communicators (those whose ssid match the disconnected ssid)
        httpCommunicatorsFromSsid(ssid).forEach { communicator ->
          // Remove the affected communicator from any facade which uses it as a communicator
          facadesById.values.forEach { it.unbindCommunicator(communicator) }
        }
        // TODO reconnect
      }

  init {
    // TODO this doesn't feel like the best place. But it is currently the only location that knows
    // about the facades. So regardless if this is done somewhere else it will need to be bubbled
    // up to here.
    scope?.launch { monitorBleConnections() }
    scope?.launch { monitorWifiConnections() }
  }

  override suspend fun getGoPro(id: GoProId): Result<GoPro> =
      communicatorsByConnection
          .filterKeys { it.id == id }
          .run {
            if (isEmpty()) return Result.failure(DeviceNotFound("No connections found with ID $id"))
            // Get or store the new gopro facade
            Result.success(
                facadesById
                    .getOrPut(id) { GoPro(id) }
                    .also { gopro ->
                      // Bind the filters communicators to the facade
                      values.forEach { communicator -> gopro.bindCommunicator(communicator) }
                      logger.i("$id communication is ready.")
                    })
          }

  override suspend fun storeConnection(connection: ConnectionDescriptor) {
    val communicator =
        communicatorsByConnection.getOrPut(connection) {
          when (connection) {
            is ConnectionDescriptor.Ble -> BleCommunicator(bleApi, connection, dispatcher)
            is ConnectionDescriptor.Http ->
                HttpCommunicator(httpApi, connection, httpClientProvider, dispatcher)
          }
        }
    getGoPro(connection.id).getOrThrow().bindCommunicator(communicator)
  }
}
