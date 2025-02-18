package com.gopro.open_gopro.domain.network

import com.benasher44.uuid.Uuid
import com.gopro.open_gopro.entity.network.ble.BleAdvertisement
import com.gopro.open_gopro.entity.network.ble.BleDevice
import com.gopro.open_gopro.entity.network.ble.BleNotification
import kotlinx.coroutines.flow.Flow

/**
 * This is the GoPro-independent BLE interface
 */
@OptIn(ExperimentalUnsignedTypes::class)
internal interface IBleApi {
    fun scan(serviceUUIDs: Set<Uuid>? = null): Result<Flow<BleAdvertisement>>

    suspend fun connect(advertisement: BleAdvertisement): Result<BleDevice>

    suspend fun enableNotifications(device: BleDevice, uuids: Set<Uuid>): Result<Unit>

    suspend fun readCharacteristic(device: BleDevice, uuid: Uuid): Result<UByteArray>

    suspend fun writeCharacteristic(device: BleDevice, uuid: Uuid, data: UByteArray): Result<Unit>

    suspend fun disconnect(device: BleDevice): Result<Unit>

    fun notificationsForConnection(device: BleDevice): Result<Flow<BleNotification>>

    fun receiveDisconnects(): Flow<BleDevice>
}