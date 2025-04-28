/* FakeBleApi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

@file:OptIn(ExperimentalUnsignedTypes::class)

package fakes

import com.benasher44.uuid.Uuid
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.AccumulatedGpBleResponse
import com.gopro.open_gopro.domain.communicator.bleCommunicator.bleFragment
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.entity.network.ble.BleAdvertisement
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.entity.network.ble.BleNotification
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.util.extensions.toPrettyHexString
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.toBleNotificationList(uuid: GpUuid): List<BleNotification> =
    this.bleFragment(BleCommunicator.MAX_PACKET_LENGTH)
        .asSequence()
        .map { BleNotification(uuid.toUuid(), it) }
        .toList()

@OptIn(ExperimentalUnsignedTypes::class)
internal sealed class BleApiSpy {
  data class Write(val device: BleDevice, val uuid: Uuid, val requestData: UByteArray) :
      BleApiSpy() {
    override fun equals(other: Any?): Boolean {
      if (this === other) return true
      if (other == null || this::class != other::class) return false

      other as Write

      if (device != other.device) return false
      if (uuid != other.uuid) return false
      if (!requestData.contentEquals(other.requestData)) return false

      return true
    }

    override fun hashCode(): Int {
      var result = device.hashCode()
      result = 31 * result + uuid.hashCode()
      result = 31 * result + requestData.contentHashCode()
      return result
    }
  }

  data class Read(val device: BleDevice, val uuid: Uuid, val responseData: UByteArray) :
      BleApiSpy() {
    override fun equals(other: Any?): Boolean {
      if (this === other) return true
      if (other == null || this::class != other::class) return false

      other as Read

      if (device != other.device) return false
      if (uuid != other.uuid) return false
      if (!responseData.contentEquals(other.responseData)) return false

      return true
    }

    override fun hashCode(): Int {
      var result = device.hashCode()
      result = 31 * result + uuid.hashCode()
      result = 31 * result + responseData.contentHashCode()
      return result
    }
  }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal class FakeBleApi(
    responses: List<List<BleNotification>> = listOf(),
    dispatcher: CoroutineDispatcher
) : IBleApi {
  val spies = mutableListOf<BleApiSpy>()
  private val notificationChannel = Channel<BleNotification>()
  private val notificationIterator = responses.listIterator()

  private var messageCounter = 0

  private var accumulatingResponse: AccumulatedGpBleResponse? = null

  var shouldWriteSucceed = true

  suspend fun sendNextMessage() {
    //        println("Fake BLE API sending message set $messageCounter.")
    notificationIterator.run {
      if (hasNext()) {
        next().forEachIndexed { index, message ->
          println("Fake BLE API sending packet $index ==> ${message.data.toPrettyHexString()}")
          notificationChannel.send(message)
          messageCounter += 1
        }
      } else {
        println("Fake BLE API Not sending next message because its queue is empty.")
      }
    }
  }

  override fun scan(serviceUUIDs: Set<Uuid>?): Result<Flow<BleAdvertisement>> {
    TODO("Not yet implemented")
  }

  override suspend fun connect(advertisement: BleAdvertisement): Result<BleDevice> {
    TODO("Not yet implemented")
  }

  override suspend fun enableNotifications(device: BleDevice, uuids: Set<Uuid>): Result<Unit> {
    TODO("Not yet implemented")
  }

  override suspend fun readCharacteristic(device: BleDevice, uuid: Uuid): Result<UByteArray> {
    spies += BleApiSpy.Read(device, uuid, ubyteArrayOf()) // TODO response
    return Result.success(ubyteArrayOf())
  }

  override suspend fun writeCharacteristic(
      device: BleDevice,
      uuid: Uuid,
      data: UByteArray
  ): Result<Unit> {
    spies += BleApiSpy.Write(device, uuid, data)
    // We need to accumulate potentially partial write payloads here and only send the next BLE
    // response on the next message
    // For now, we assume there is only ever one concurrent accumulating response
    accumulatingResponse =
        (accumulatingResponse ?: AccumulatedGpBleResponse(GpUuid.fromUuid(uuid)!!)).apply {
          accumulate(data)
        }
    if (accumulatingResponse?.isReceived == true) {
      sendNextMessage()
      accumulatingResponse = null
    }
    return Result.success(Unit)
  }

  override suspend fun disconnect(device: BleDevice): Result<Unit> {
    TODO("Not yet implemented")
  }

  override fun notificationsForConnection(device: BleDevice): Result<Flow<BleNotification>> =
      Result.success(
          flow {
            while (true) {
              emit(notificationChannel.receive())
            }
          })

  override fun receiveDisconnects(): Flow<BleDevice> = flow {}
}
