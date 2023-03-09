/* Tutorial3ParseBleTlvResponses.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.DataStore
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.serialization.encodeToString
import timber.log.Timber
import java.io.File
import java.util.*
import kotlin.properties.Delegates.notNull

@OptIn(ExperimentalUnsignedTypes::class)
sealed class Response<T > {
    private enum class Header(val value: UByte) {
        GENERAL(0b00U), EXT_13(0b01U), EXT_16(0b10U), RESERVED(0b11U);

        companion object {
            private val valueMap: Map<UByte, Header> by lazy {
                Header.values().associateBy { it.value }
            }

            fun fromValue(value: Int) = valueMap.getValue(value.toUByte())
        }
    }

    private enum class Mask(val value: UByte) {
        Header(0b01100000U),
        Continuation(0b10000000U),
        GenLength(0b00011111U),
        Ext13Byte0(0b00011111U)
    }

    private var bytesRemaining = 0
    protected var packet = ubyteArrayOf()
    abstract val data: T
    var id by notNull<Int>()
        protected set
    var status by notNull<Int>()
        protected set

    val isReceived get() = bytesRemaining == 0
    var isParsed = false
        protected set

    override fun toString() = prettyJson.encodeToString(data.toJsonElement())

    fun accumulate(data: UByteArray) {
        var buf = data
        // If this is a continuation packet
        if (data.first().and(Mask.Continuation.value) == Mask.Continuation.value) {
            buf = buf.drop(1).toUByteArray() // Pop the header byte
        } else {
            // This is a new packet so start with empty array
            packet = ubyteArrayOf()
            when (Header.fromValue((buf.first() and Mask.Header.value).toInt() shr 5)) {
                Header.GENERAL -> {
                    bytesRemaining = buf[0].and(Mask.GenLength.value).toInt()
                    buf = buf.drop(1).toUByteArray()
                }
                Header.EXT_13 -> {
                    bytesRemaining = ((buf[0].and(Mask.Ext13Byte0.value)
                        .toLong() shl 8) or buf[1].toLong()).toInt()
                    buf = buf.drop(2).toUByteArray()
                }
                Header.EXT_16 -> {
                    bytesRemaining = ((buf[1].toLong() shl 8) or buf[2].toLong()).toInt()
                    buf = buf.drop(3).toUByteArray()
                }
                Header.RESERVED -> {
                    throw Exception("Unexpected RESERVED header")
                }
            }
        }
        // Accumulate the payload now that headers are handled and dropped
        packet += buf
        bytesRemaining -= buf.size
        Timber.i("Received packet of length ${buf.size}. $bytesRemaining bytes remaining")

        if (bytesRemaining < 0) {
            throw Exception("Unrecoverable parsing error. Received too much data.")
        }
    }

    abstract fun parse()

    class Complex : Response<MutableList<UByteArray>>() {
        override val data: MutableList<UByteArray> = mutableListOf()

        override fun parse() {
            require(isReceived)
            // Parse header bytes
            id = packet[0].toInt()
            status = packet[1].toInt()
            var buf = packet.drop(2)
            // Parse remaining packet
            while (buf.isNotEmpty()) {
                // Get each parameter's ID and length
                val paramLen = buf[0].toInt()
                buf = buf.drop(1)
                // Get the parameter's value
                val paramVal = buf.take(paramLen)
                // Store in data list
                data += paramVal.toUByteArray()
                // Advance the buffer for continued parsing
                buf = buf.drop(paramLen)
            }
            isParsed = true
        }
    }

    class Query : Response<MutableMap<UByte, UByteArray>>() {
        override val data: MutableMap<UByte, UByteArray> = mutableMapOf()

        override fun parse() {
            require(isReceived)
            id = packet[0].toInt()
            status = packet[1].toInt()
            // Parse remaining packet
            var buf = packet.drop(2)
            while (buf.isNotEmpty()) {
                // Get each parameter's ID and length
                val paramId = buf[0]
                val paramLen = buf[1].toInt()
                buf = buf.drop(2)
                // Get the parameter's value
                val paramVal = buf.take(paramLen)
                // Store in data dict for access later
                data[paramId] = paramVal.toUByteArray()
                // Advance the buffer for continued parsing
                buf = buf.drop(paramLen)
            }
            isParsed = true
        }
    }

    companion object {
        fun fromUuid(uuid: GoProUUID): Response<*> =
            when (uuid) {
                GoProUUID.CQ_COMMAND_RSP -> Complex()
                GoProUUID.CQ_QUERY_RSP -> Query()
                else -> throw Exception("Not supported")
            }
    }

}

@OptIn(ExperimentalUnsignedTypes::class)
class Tutorial3ParseBleTlvResponses(number: Int, name: String, prerequisites: List<Prerequisite>) :
    Tutorial(number, name, prerequisites) {
    private val receivedResponse: Channel<Response<*>> = Channel()
    private var response: Response<*>? = null

    @OptIn(ExperimentalUnsignedTypes::class)
    private fun tlvResponseNotificationHandler(characteristic: UUID, data: UByteArray) {
        GoProUUID.fromUuid(characteristic)?.let { uuid ->
            // If response is currently empty, create a new one
            response = response ?: Response.fromUuid(uuid)
        }
            ?: return // We don't care about non-GoPro characteristics (i.e. the BT Core Battery service)

        Timber.d("Received response on $characteristic: ${data.toHexString()}")

        response?.let { rsp ->
            rsp.accumulate(data)
            if (rsp.isReceived) {
                rsp.parse()

                // If the response has success status...
                if (rsp.status == 0) Timber.i("Received the expected successful response")
                else Timber.i("Received unexpected response")

                // Notify the command sender the the procedure is complete
                response = null // Clear for next command
                CoroutineScope(Dispatchers.IO).launch { receivedResponse.send(rsp) }
            }
        } ?: throw Exception("This should be impossible")
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    private val bleListeners by lazy {
        BleEventListener().apply {
            onNotification = ::tlvResponseNotificationHandler
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    @RequiresPermission(allOf = ["android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"])
    override suspend fun perform(appContainer: AppContainer): File? {
        val ble = appContainer.ble
        val goproAddress =
            DataStore.connectedGoPro ?: throw Exception("No GoPro is currently connected")

        // Register our notification handler callback for characteristic change updates
        ble.registerListener(goproAddress, bleListeners)

        Timber.i("Getting the Open GoPro version")
        val getVersion = ubyteArrayOf(0x01U, 0x51U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, getVersion)
        val version = receivedResponse.receive() as Response.Complex // Wait to receive response
        val major = version.data[0].first().toInt()
        val minor = version.data[1].first().toInt()
        Timber.i("Got the Open GoPro version successfully: $major.$minor")

        Timber.i("Getting the camera's settings")
        val getCameraSettings = ubyteArrayOf(0x01U, 0x12U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, getCameraSettings)
        val settings = receivedResponse.receive()
        Timber.i("Got the camera's settings successfully")
        Timber.i(settings.toString())

        Timber.i("Getting the camera's statuses")
        val getCameraStatuses = ubyteArrayOf(0x01U, 0x13U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, getCameraStatuses)
        val statuses = receivedResponse.receive()
        Timber.i("Got the camera's statuses successfully")
        Timber.i(statuses.toString())

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListeners)
        return null
    }
}