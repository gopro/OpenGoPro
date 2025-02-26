/* KableBle.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.network

import com.benasher44.uuid.Uuid
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.entity.network.ble.BleAdvertisement
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.util.GpCommonBase
import com.gopro.open_gopro.util.IGpCommonBase
import com.gopro.open_gopro.util.extensions.toPrettyHexString
import com.juul.kable.Advertisement as KableAdvertisement
import com.juul.kable.Characteristic
import com.juul.kable.Peripheral
import com.juul.kable.Scanner
import com.juul.kable.State as KableState
import com.juul.kable.WriteType
import com.juul.kable.logs.Logging
import com.juul.kable.logs.SystemLogEngine
import com.juul.kable.peripheral
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.cancel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.job
import kotlinx.coroutines.launch
import kotlinx.coroutines.withTimeout

// https://github.com/JuulLabs/kable/blob/5cb15670216a4566d5ace188f0e2b87b1ed70c50/kable-core/src/commonMain/kotlin/Advertisement.kt#L4

private const val CONNECTION_TIMEOUT_MS = 30000L

@OptIn(ExperimentalUnsignedTypes::class)
private class KableDevice(private val adv: KableAdvertisement, dispatcher: CoroutineDispatcher) :
    BleDevice, IGpCommonBase by GpCommonBase("KableDevice", dispatcher) {
  // TODO this has been fixed. Update Kable and remove.
  // Intermediary scope needed until https://github.com/JuulLabs/kable/issues/577 is resolved.
  private val peripheralScope = CoroutineScope(Job())
  override val scope =
      CoroutineScope(
          dispatcher + peripheralScope.coroutineContext + Job(peripheralScope.coroutineContext.job))

  val notifications = MutableSharedFlow<BleNotification>()
  lateinit var peripheral: Peripheral

  // Platform specific ID
  override val id
    get() = peripheral.identifier.toString()

  private val characteristicByUuid: Map<Uuid, Characteristic> by lazy {
    // TODO there is almost certainly a clean functional way to do this
    val map = mutableMapOf<Uuid, Characteristic>()
    peripheral.services?.let { services ->
      for (service in services) {
        for (char in service.characteristics) {
          map[char.characteristicUuid] = char
        }
      }
    } ?: throw Exception("Services have not yet been discovered")
    map
  }

  suspend fun connect(): Result<Unit> =
      try {
        withTimeout(CONNECTION_TIMEOUT_MS) {
          logger.d("Establishing BLE connection to ${adv.identifier}")
          // We tried this as a callback flow but onServicesDiscovered sometimes comes before
          // peripheral.connect
          // Channel will handle both of these cases
          val servicesDiscovered = Channel<Unit>(1)
          peripheral =
              scope.peripheral(adv) {
                logging { level = Logging.Level.Data }
                // Send the channel when the services have been discovered
                onServicesDiscovered { servicesDiscovered.send(Unit) }
              }
          peripheral.connect()
          logger.d("BLE connection established. Waiting for services to be discovered")
          servicesDiscovered.receive()
          logger.d("Services discovered.")
          Result.success(Unit)
        }
      } catch (exc: TimeoutCancellationException) {
        logger.e("Connection establishment timed out")
        Result.failure(exc)
      }

  @OptIn(ExperimentalUnsignedTypes::class)
  fun enableNotifications(uuids: Set<Uuid>): Boolean {
    uuids.forEach { uuid ->
      characteristicByUuid[uuid]?.let { characteristic ->
        logger.d("Enabling notifications for ${characteristic.characteristicUuid}")
        scope.launch {
          peripheral
              .observe(characteristic)
              .catch { exc -> logger.e(exc.toString()) }
              .onEach {
                logger.d(
                    "Received notification ${it.toPrettyHexString()} on ${characteristic.characteristicUuid}")
              }
              .collect { data ->
                // Forward to our observers.
                notifications.emit(BleNotification(uuid, data.toUByteArray()))
              }
        }
      }
          ?: run {
            logger.e("Could not find characteristic with uuid: $uuid")
            return false
          }
    }
    return true
  }

  suspend fun readCharacteristic(uuid: Uuid): UByteArray? =
      characteristicByUuid[uuid]?.let { peripheral.read(it) }?.toUByteArray()

  suspend fun writeCharacteristic(uuid: Uuid, data: UByteArray): Boolean =
      characteristicByUuid[uuid]?.let {
        peripheral.write(it, data.toByteArray(), WriteType.WithResponse)
      } != null

  suspend fun disconnect(): Boolean {
    peripheral.disconnect()
    scope.cancel() // TODO do we really want / need to do this here?
    return true // TODO how to wait for / check disconnection?
  }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal class KableBle(private val dispatcher: CoroutineDispatcher) :
    IBleApi, IGpCommonBase by GpCommonBase("KableBle", dispatcher) {

  // TODO instead can we just return the Kable Device and cast Ble Devices to Kable devices when
  // we receive them
  // Kable devices by peripheral's platform-specific identifier converted to string
  private val deviceMap = mutableMapOf<String, KableDevice>()

  // Kable advertisements by advertisement's platform-specific identifier converted to string
  private val advMap = mutableMapOf<String, KableAdvertisement>()

  private val deviceStateChanges = MutableSharedFlow<Pair<KableDevice, KableState>>()

  private suspend fun monitorConnections() =
      deviceStateChanges
          .onEach { (device, state) -> logger.d("Device ${device.id} state change: $state") }
          // We currently only care about disconnects
          .filter { (_, state) -> state is KableState.Disconnected }
          // Remove the now disconnected device from the map
          .collect { (device, _) -> deviceMap.remove(device.id) }

  init {
    scope?.launch { monitorConnections() }
  }

  override fun notificationsForConnection(device: BleDevice): Result<Flow<BleNotification>> =
      deviceMap[device.id]?.notifications?.let { Result.success(it) }
          ?: Result.failure(Exception("Could not find device"))

  override fun receiveDisconnects(): Flow<BleDevice> =
      deviceStateChanges
          .filter { (_, state) -> state is KableState.Disconnected }
          .map { (device, _) -> device }

  override fun scan(serviceUUIDs: Set<Uuid>?): Result<Flow<BleAdvertisement>> =
      Result.success(
          Scanner {
                filters { match { serviceUUIDs?.let { services = serviceUUIDs.toList() } } }
                logging {
                  engine = SystemLogEngine
                  level = Logging.Level.Data
                  format = Logging.Format.Multiline
                }
              }
              .advertisements
              .onStart { advMap.clear() }
              .filter { it.name != null }
              .onEach {
                logger.d("Received advertisement: ${it.identifier} ==> ${it.name!!}")
                advMap[it.identifier.toString()] = it
              }
              .map { adv ->
                object : BleAdvertisement {
                  override val id = adv.identifier.toString()
                  override val name: String = adv.name!!
                  override val manufacturerData = adv.manufacturerData?.data
                  override val service: Map<Uuid, ByteArray?>? =
                      serviceUUIDs?.associateWith { adv.serviceData(it) }
                }
              })

  override suspend fun connect(advertisement: BleAdvertisement): Result<BleDevice> {
    val kableAdv =
        advMap[advertisement.id]
            ?: return Result.failure(Exception("advertisement ${advertisement.id} not found"))
    val kableDevice = KableDevice(kableAdv, dispatcher)
    return kableDevice.connect().map {
      // Forward any connection state updates
      scope?.launch {
        kableDevice.peripheral.state.collect { deviceStateChanges.emit(Pair(kableDevice, it)) }
      }
      // Add our device to the map
      deviceMap[kableDevice.id] = kableDevice
      // Return the device
      kableDevice
    }
  }

  override suspend fun enableNotifications(device: BleDevice, uuids: Set<Uuid>): Result<Unit> =
      deviceMap[device.id]?.enableNotifications(uuids)?.let { Result.success(Unit) }
          ?: Result.failure(Exception("connected $device does not exist"))

  override suspend fun readCharacteristic(device: BleDevice, uuid: Uuid): Result<UByteArray> =
      deviceMap[device.id]?.readCharacteristic(uuid)?.let { Result.success(it) }
          ?: Result.failure(Exception("connected $device does not exist"))

  override suspend fun writeCharacteristic(
      device: BleDevice,
      uuid: Uuid,
      data: UByteArray
  ): Result<Unit> =
      deviceMap[device.id]?.writeCharacteristic(uuid, data)?.let { Result.success(Unit) }
          ?: Result.failure(Exception("connected $device does not exist"))

  override suspend fun disconnect(device: BleDevice): Result<Unit> =
      deviceMap[device.id]?.disconnect()?.let { Result.success(Unit) }
          ?: Result.failure(Exception("connected $device does not exist"))
}
