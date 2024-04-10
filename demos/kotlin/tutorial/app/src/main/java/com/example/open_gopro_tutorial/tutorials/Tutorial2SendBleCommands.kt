/* Tutorial2SendBleCommands.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.DataStore
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.util.GoProUUID
import com.example.open_gopro_tutorial.util.toHexString
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import timber.log.Timber
import java.io.File
import java.util.*

@OptIn(ExperimentalUnsignedTypes::class)
class Tutorial2SendBleCommands(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    private val receivedData: Channel<UByteArray> = Channel()

    @OptIn(ExperimentalUnsignedTypes::class)
    private fun naiveNotificationHandler(characteristic: UUID, data: UByteArray) {
        Timber.d("Received response on $characteristic: ${data.toHexString()}")
        if ((characteristic == GoProUUID.CQ_COMMAND_RSP.uuid)) {
            Timber.d("Command status received")
            CoroutineScope(Dispatchers.IO).launch { receivedData.send(data) }
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    private val bleListeners by lazy {
        BleEventListener().apply {
            onNotification = ::naiveNotificationHandler
        }
    }

    private fun checkStatus(data: UByteArray) =
        if (data[2].toUInt() == 0U) Timber.i("Command sent successfully")
        else Timber.e("Command Failed")

    @OptIn(ExperimentalUnsignedTypes::class)
    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val ble = appContainer.ble
        val goproAddress =
            DataStore.connectedGoPro ?: throw Exception("No GoPro is currently connected")

        // Register our notification handler callback for characteristic change updates
        ble.registerListener(goproAddress, bleListeners)

        // Set the shutter
        Timber.i("Setting the shutter on")
        val setShutterOnCmd = ubyteArrayOf(0x03U, 0x01U, 0x01U, 0x01U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setShutterOnCmd)
        // Wait to receive the notification response, then check its status
        checkStatus(receivedData.receive())

        delay(2000)

        Timber.i("Setting the shutter off")
        val setShutterOffCmd = ubyteArrayOf(0x03U, 0x01U, 0x01U, 0x00U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setShutterOffCmd)
        // Wait to receive the notification response, then check its status
        checkStatus(receivedData.receive())

        delay(3000)

        // Load Preset Group
        Timber.i("Loading Video Preset Group")
        val loadPreset = ubyteArrayOf(0x04U, 0x3EU, 0x02U, 0x03U, 0xE8U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, loadPreset)
        // Wait to receive the notification response, then check its status
        checkStatus(receivedData.receive())

        // Set the Resolution
        Timber.i("Setting resolution to 1080")
        val setResolution = ubyteArrayOf(0x03U, 0x02U, 0x01U, 0x09U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setResolution)
        // Wait to receive the notification response, then check its status
        checkStatus(receivedData.receive())

        // Set the FPS
        Timber.i("Setting the FPS to 240")
        val setFps = ubyteArrayOf(0x03U, 0x03U, 0x01U, 0x00U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setFps)
        // Wait to receive the notification response, then check its status
        checkStatus(receivedData.receive())

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListeners)
        return null
    }
}