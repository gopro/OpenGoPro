/* Tutorial5ConnectWifi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.DataStore
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.util.GoProUUID
import com.example.open_gopro_tutorial.util.decodeToString
import com.example.open_gopro_tutorial.util.toHexString
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import timber.log.Timber
import java.io.File
import java.util.*

@OptIn(ExperimentalUnsignedTypes::class)
class Tutorial5ConnectWifi(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    private val receivedData: Channel<UByteArray> = Channel()

    @OptIn(ExperimentalUnsignedTypes::class)
    private fun naiveNotificationHandler(characteristic: UUID, data: UByteArray) {
        // Only process GoPro UUID's
        if (characteristic !in GoProUUID.values().map { it.uuid }) return

        Timber.d("Received response on $characteristic: ${data.toHexString()}")
        if ((characteristic == GoProUUID.CQ_COMMAND_RSP.uuid) && (data[2].toUInt() == 0U)) {
            Timber.d("Command sent successfully")
            CoroutineScope(Dispatchers.IO).launch { receivedData.send(data) }
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    private val bleListener by lazy {
        BleEventListener().apply {
            onNotification = ::naiveNotificationHandler
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val ble = appContainer.ble
        val wifi = appContainer.wifi
        val goproAddress =
            DataStore.connectedGoPro ?: throw Exception("No GoPro is currently connected")

        // Register to get BLE notification updates
        ble.registerListener(goproAddress, bleListener)

        // Get the password and ssid as strings
        lateinit var password: String
        lateinit var ssid: String
        Timber.i("Getting the password")
        ble.readCharacteristic(goproAddress, GoProUUID.WIFI_AP_PASSWORD.uuid)
            .onSuccess { password = it.decodeToString() }.onFailure { throw it }
        Timber.i("Password is $password")
        Timber.i("Getting the SSID")
        ble.readCharacteristic(goproAddress, GoProUUID.WIFI_AP_SSID.uuid)
            .onSuccess { ssid = it.decodeToString() }.onFailure { throw it }
        Timber.i("SSID is $ssid")

        // Write to the Command Request BleUUID to enable WiFi AP on the camera
        Timber.i("Enabling the camera's Wifi AP")
        val enableWifiCommand = ubyteArrayOf(0x03U, 0x17U, 0x01U, 0x01U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, enableWifiCommand)
        receivedData.receive()

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListener)

        // Now connect to the camera's Wifi
        Timber.i("Connecting to the camera's Wifi AP")
        wifi.connect(ssid, password)
        Timber.i("Wifi is ready for communication!!")

        return null
    }
}