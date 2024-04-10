/* Tutorial3ParseBleTlvResponses.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.tutorials

import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.DataStore
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.util.GoProUUID
import com.example.open_gopro_tutorial.util.decodeToString
import com.example.open_gopro_tutorial.util.prettyJson
import com.example.open_gopro_tutorial.util.toHexString
import com.example.open_gopro_tutorial.util.toInt
import com.example.open_gopro_tutorial.util.toJsonElement
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.serialization.encodeToString
import timber.log.Timber
import java.io.File
import java.util.UUID
import kotlin.properties.Delegates.notNull

@OptIn(ExperimentalUnsignedTypes::class)
sealed class Response(val uuid: GoProUUID) {
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
    var rawBytes = ubyteArrayOf()
        protected set

    val isReceived get() = bytesRemaining == 0

    fun accumulate(data: UByteArray) {
        var buf = data
        // If this is a continuation packet
        if (data.first().and(Mask.Continuation.value) == Mask.Continuation.value) {
            buf = buf.drop(1).toUByteArray() // Pop the header byte
        } else {
            // This is a new packet so start with empty array
            rawBytes = ubyteArrayOf()
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
        rawBytes += buf
        bytesRemaining -= buf.size
        Timber.d("Received packet of length ${buf.size}. $bytesRemaining bytes remaining")

        if (bytesRemaining < 0) {
            throw Exception("Unrecoverable parsing error. Received too much data.")
        }
    }

    open class Tlv(uuid: GoProUUID) : Response(uuid) {
        var payload = ubyteArrayOf()
            private set
        var id by notNull<Int>()
            private set
        var status by notNull<Int>()
            private set

        open fun parse() {
            require(isReceived)
            id = rawBytes[0].toInt()
            status = rawBytes[1].toInt()
            // Store remainder as payload for further parsing later
            payload = rawBytes.drop(2).toUByteArray()
        }

        override fun toString(): String = "ID: $id, Status: $status, Payload: ${payload.toHexString()}"
    }

    class Query(uuid: GoProUUID) : Tlv(uuid) {
        val data: MutableMap<UByte, UByteArray> = mutableMapOf()
        override fun toString() = prettyJson.encodeToString(data.toJsonElement())

        override fun parse() {
            super.parse()
            var buf = payload.toList()
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
        }
    }

    class Unknown(uuid: GoProUUID): Response(uuid) {}

    companion object {
        fun muxByUuid(uuid: GoProUUID) : Response {
            return when (uuid) {
                GoProUUID.CQ_SETTING_RSP, GoProUUID.CQ_COMMAND_RSP -> Tlv(uuid)
                GoProUUID.CQ_QUERY_RSP -> Query(uuid)
                else -> Unknown(uuid)
            }
        }
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
data class OpenGoProVersion(val minor: Int, val major: Int) {
    companion object {
        fun fromBytes(data: UByteArray): OpenGoProVersion {
            var buf = data.toUByteArray()
            val majorLen = buf[0].toInt()
            buf = buf.drop(1).toUByteArray()
            val major = buf.take(majorLen).toInt()
            buf = buf.drop(1).toUByteArray()
            val minorLen = buf[0].toInt()
            buf = buf.drop(1).toUByteArray()
            val minor = buf.take(minorLen).toInt()
            return OpenGoProVersion(minor, major)
        }
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
data class HardwareInfo(
    val modelNumber: Int,
    val modelName: String,
    val firmwareVersion: String,
    val serialNumber: String,
    val apSsid: String,
    val apMacAddress: String
) {
    companion object {
        fun fromBytes(data: UByteArray): HardwareInfo {
            // Parse header bytes
            var buf = data.toUByteArray()
            // Get model number
            val modelNumLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val model = buf.take(modelNumLength).toInt()
            buf = buf.drop(modelNumLength).toUByteArray()
            // Get model name
            val modelNameLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val modelName = buf.take(modelNameLength).decodeToString()
            buf = buf.drop(modelNameLength).toUByteArray()
            // Advance past deprecated bytes
            val deprecatedLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            buf = buf.drop(deprecatedLength).toUByteArray()
            // Get firmware version
            val firmwareLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val firmware = buf.take(firmwareLength).decodeToString()
            buf = buf.drop(firmwareLength).toUByteArray()
            // Get serial number
            val serialLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val serial = buf.take(serialLength).decodeToString()
            buf = buf.drop(serialLength).toUByteArray()
            // Get AP SSID
            val ssidLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val ssid = buf.take(ssidLength).decodeToString()
            buf = buf.drop(ssidLength).toUByteArray()
            // Get MAC Address
            val macLength = buf.first().toInt()
            buf = buf.drop(1).toUByteArray()
            val mac = buf.take(macLength).decodeToString()

            return HardwareInfo(model, modelName, firmware, serial, ssid, mac)
        }
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
class Tutorial3ParseBleTlvResponses(
    number: Int,
    name: String,
    prerequisites: List<Prerequisite>
) :
    Tutorial(number, name, prerequisites) {
    private val receivedResponses: Channel<Response> = Channel()
    private val responsesByUuid = GoProUUID.mapByUuid { Response.muxByUuid(it) }

    @OptIn(ExperimentalUnsignedTypes::class)
    private fun notificationHandler(characteristic: UUID, data: UByteArray) {
        // Get the UUID (assuming it is a GoPro UUID)
        val uuid = GoProUUID.fromUuid(characteristic) ?: return
        Timber.d("Received response on $uuid")

        responsesByUuid[uuid]?.let { response ->
            response.accumulate(data)
            if (response.isReceived) {
                if (uuid == GoProUUID.CQ_COMMAND_RSP) {
                    CoroutineScope(Dispatchers.IO).launch { receivedResponses.send(response) }
                } else {
                    Timber.e("Unexpected Response")
                }
                responsesByUuid[uuid] = Response.muxByUuid(uuid)
            }
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    private val bleListeners by lazy {
        BleEventListener().apply {
            onNotification = ::notificationHandler
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
        val versionRequest = ubyteArrayOf(0x01U, 0x51U)
        ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, versionRequest)
        // Wait to receive response the parse it
        var tlvResponse = receivedResponses.receive() as Response.Tlv
        tlvResponse.parse()
        Timber.i("Received response: $tlvResponse")
        val version = OpenGoProVersion.fromBytes(tlvResponse.payload)
        Timber.i("Got the Open GoPro version successfully: ${version.major}.${version.minor}")

        Timber.i("Getting the Hardware Info")
        val hardwareInfoRequest = ubyteArrayOf(0x01U, 0x3CU)
        ble.writeCharacteristic(
            goproAddress,
            GoProUUID.CQ_COMMAND.uuid,
            hardwareInfoRequest
        )
        // Wait to receive response the parse it
        tlvResponse = receivedResponses.receive() as Response.Tlv
        tlvResponse.parse()
        val hardwareInfo = HardwareInfo.fromBytes(tlvResponse.payload)
        Timber.i("Got the Hardware Info successfully: $hardwareInfo")

        // Other tutorials will use their own notification handler so unregister ours now
        ble.unregisterListener(bleListeners)
        return null
    }
}