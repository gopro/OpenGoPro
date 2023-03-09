/* Tutorial4BleQueries.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.DataStore
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.network.Bluetooth
import com.example.open_gopro_tutorial.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import timber.log.Timber
import java.io.File
import java.util.*

private const val RESOLUTION_ID: UByte = 2U

@OptIn(ExperimentalUnsignedTypes::class)
class Tutorial4BleQueries(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    private enum class Resolution(val value: UByte) {
        RES_4K(1U),
        RES_2_7K(4U),
        RES_2_7K_4_3(6U),
        RES_1080(9U),
        RES_4K_4_3(18U),
        RES_5K(24U);

        companion object {
            private val valueMap: Map<UByte, Resolution> by lazy { values().associateBy { it.value } }

            fun fromValue(value: UByte) = valueMap.getValue(value)
        }
    }

    private val receivedResponse: Channel<Response.Query> = Channel()
    private var response: Response.Query? = null
    private lateinit var resolution: Resolution

    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    private suspend fun performPollingTutorial(ble: Bluetooth, goproAddress: String) {
        @OptIn(ExperimentalUnsignedTypes::class)
        fun resolutionPollingNotificationHandler(characteristic: UUID, data: UByteArray) {
            GoProUUID.fromUuid(characteristic)?.let {
                // If response is currently empty, create a new one
                response =
                    response ?: Response.Query() // We're only handling queries in this tutorial
            }
                ?: return // We don't care about non-GoPro characteristics (i.e. the BT Core Battery service)

            Timber.d("Received response on $characteristic: ${data.toHexString()}")

            response?.let { rsp ->
                rsp.accumulate(data)
                if (rsp.isReceived) {
                    rsp.parse()

                    // If this is a query response, it must contain a resolution value
                    if (characteristic == GoProUUID.CQ_QUERY_RSP.uuid) {
                        Timber.i("Received resolution query response")
                    }
                    // If this is a setting response, it will just show the status
                    else if (characteristic == GoProUUID.CQ_SETTING_RSP.uuid) {
                        Timber.i("Command sent successfully")
                    }
                    // Anything else is unexpected. This shouldn't happen
                    else {
                        Timber.i("Received unexpected response")
                    }

                    // Notify the command sender the the procedure is complete
                    response = null // Clear for next command
                    CoroutineScope(Dispatchers.IO).launch { receivedResponse.send(rsp) }
                }
            }
        }

        @OptIn(ExperimentalUnsignedTypes::class)
        val bleListeners by lazy {
            BleEventListener().apply {
                onNotification = ::resolutionPollingNotificationHandler
            }
        }

        // Register our notification handler callback for characteristic change updates
        ble.registerListener(goproAddress, bleListeners)

        // Write to query BleUUID to poll the current resolution
        Timber.i("Polling the current resolution")
        val pollResolution = ubyteArrayOf(0x02U, 0x12U, RESOLUTION_ID)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, pollResolution)
        resolution = Resolution.fromValue(
            receivedResponse.receive().data.getValue(RESOLUTION_ID).first()
        )
        Timber.i("Camera resolution is $resolution")

        // Write to command request BleUUID to change the video resolution (either to 1080 or 2.7K)
        val newResolution =
            if (resolution == Resolution.RES_2_7K) Resolution.RES_1080 else Resolution.RES_2_7K
        Timber.i("Changing the resolution to $newResolution")
        val setResolution = ubyteArrayOf(0x03U, RESOLUTION_ID, 0x01U, newResolution.value)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_SETTING.uuid, setResolution)
        val setResolutionResponse = receivedResponse.receive()
        if (setResolutionResponse.status == 0) {
            Timber.i("Resolution successfully changed")
        } else {
            Timber.e("Failed to set resolution")
        }

        // Now let's poll until an update occurs
        Timber.i("Polling the resolution until it changes")
        while (resolution != newResolution) {
            ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, pollResolution)
            resolution = Resolution.fromValue(
                receivedResponse.receive().data.getValue(RESOLUTION_ID).first()
            )
            Timber.i("Camera resolution is currently $resolution")
        }

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListeners)
    }

    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    private suspend fun performRegisteringForAsyncUpdatesTutorial(
        ble: Bluetooth, goproAddress: String
    ) {
        @OptIn(ExperimentalUnsignedTypes::class)
        fun resolutionRegisteringNotificationHandler(characteristic: UUID, data: UByteArray) {
            GoProUUID.fromUuid(characteristic)?.let {
                // If response is currently empty, create a new one
                response = response ?: Response.Query() // We're only handling queries in this tutorial
            } ?: return // We don't care about non-GoPro characteristics (i.e. the BT Core Battery service)

            Timber.d("Received response on $characteristic: ${data.toHexString()}")

            response?.let { rsp ->
                rsp.accumulate(data)

                if (rsp.isReceived) {
                    rsp.parse()

                    // If this is a query response, it must contain a resolution value
                    if (characteristic == GoProUUID.CQ_QUERY_RSP.uuid) {
                        Timber.i("Received resolution query response")
                        resolution = Resolution.fromValue(rsp.data.getValue(RESOLUTION_ID).first())
                        Timber.i("Resolution is now $resolution")
                    }
                    // If this is a setting response, it will just show the status
                    else if (characteristic == GoProUUID.CQ_SETTING_RSP.uuid) {
                        Timber.i("Command sent successfully")
                    }
                    // Anything else is unexpected. This shouldn't happen
                    else {
                        Timber.i("Received unexpected response")
                    }

                    // Notify the command sender the the procedure is complete
                    response = null
                    CoroutineScope(Dispatchers.IO).launch { receivedResponse.send(rsp) }
                }
            }
        }

        @OptIn(ExperimentalUnsignedTypes::class)
        val bleListeners by lazy {
            BleEventListener().apply {
                onNotification = ::resolutionRegisteringNotificationHandler
            }
        }

        // Register our notification handler callback for characteristic change updates
        ble.registerListener(goproAddress, bleListeners)

        // Register with the GoPro for updates when resolution updates occur
        Timber.i("Registering for resolution value updates")
        val registerResolutionUpdates = ubyteArrayOf(0x02U, 0x52U, RESOLUTION_ID)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, registerResolutionUpdates)
        Timber.i("Camera resolution is $resolution")

        // Write to command request BleUUID to change the video resolution (either to 1080 or 2.7K)
        val newResolution =
            if (resolution == Resolution.RES_2_7K) Resolution.RES_1080 else Resolution.RES_2_7K
        Timber.i("Changing the resolution to $newResolution")
        val setResolution = ubyteArrayOf(0x03U, RESOLUTION_ID, 0x01U, newResolution.value)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_SETTING.uuid, setResolution)
        val setResolutionResponse = receivedResponse.receive()
        if (setResolutionResponse.status == 0) {
            Timber.i("Resolution successfully changed")
        } else {
            Timber.e("Failed to set resolution")
        }

        // Verify we receive the update from the camera when the resolution changes
        while (resolution != newResolution) {
            Timber.i("Waiting for camera to inform us about the resolution change")
            receivedResponse.receive()
        }

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListeners)
    }

    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val ble = appContainer.ble
        val goproAddress =
            DataStore.connectedGoPro ?: throw Exception("No GoPro is currently connected")

        performPollingTutorial(ble, goproAddress)

        performRegisteringForAsyncUpdatesTutorial(ble, goproAddress)

        return null
    }
}