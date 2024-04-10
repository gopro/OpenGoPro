/* Extensions.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.util

import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.json.*
import timber.log.Timber
import java.util.*

/**
 * Most of these are taken from https://punchthrough.com/android-ble-guide/
 */

@OptIn(ExperimentalUnsignedTypes::class)
fun Int.toUByteArrayBigEndian(size: Int): UByteArray {
    var bytes = byteArrayOf()
    for (i in 1..size) {
        bytes += (this and (0xFF shl (i * 8))).toByte()
    }
    return bytes.toUByteArray()
}

fun List<UByte>.toInt(): Int {
    var value = 0
    this.forEachIndexed { index, byte ->
        value += (byte.toInt() shl (index * 8))
    }
    return value
}


fun ByteArray.toHexString(): String = joinToString(separator = ":") { String.format("%02X", it) }

@OptIn(ExperimentalUnsignedTypes::class)
fun UByteArray.toHexString(): String = this.toByteArray().toHexString()

@OptIn(ExperimentalUnsignedTypes::class)
fun UByteArray.decodeToString(): String = this.toByteArray().decodeToString()

@OptIn(ExperimentalUnsignedTypes::class)
fun List<UByte>.decodeToString() = this.toUByteArray().decodeToString()

fun BluetoothGatt.findCharacteristic(uuid: UUID): BluetoothGattCharacteristic? {
    services?.forEach { service ->
        service.characteristics?.firstOrNull { characteristic ->
            characteristic.uuid == uuid
        }?.let { matchingCharacteristic ->
            return matchingCharacteristic
        }
    }
    return null
}

fun BluetoothGattDescriptor.containsPermission(permission: Int): Boolean =
    permissions and permission != 0

fun BluetoothGattDescriptor.isReadable(): Boolean =
    containsPermission(BluetoothGattDescriptor.PERMISSION_READ)

fun BluetoothGattDescriptor.isWritable(): Boolean =
    containsPermission(BluetoothGattDescriptor.PERMISSION_WRITE)

fun BluetoothGattDescriptor.printProperties(): String = mutableListOf<String>().apply {
    if (isReadable()) add("READABLE")
    if (isWritable()) add("WRITABLE")
    if (isEmpty()) add("EMPTY")
}.joinToString()

fun BluetoothGattCharacteristic.isReadable(): Boolean =
    containsProperty(BluetoothGattCharacteristic.PROPERTY_READ)

fun BluetoothGattCharacteristic.isWritable(): Boolean =
    containsProperty(BluetoothGattCharacteristic.PROPERTY_WRITE)

fun BluetoothGattCharacteristic.isWritableWithoutResponse(): Boolean =
    containsProperty(BluetoothGattCharacteristic.PROPERTY_WRITE_NO_RESPONSE)

fun BluetoothGattCharacteristic.isIndicatable(): Boolean =
    containsProperty(BluetoothGattCharacteristic.PROPERTY_INDICATE)

fun BluetoothGattCharacteristic.isNotifiable(): Boolean =
    containsProperty(BluetoothGattCharacteristic.PROPERTY_NOTIFY)

fun BluetoothGattCharacteristic.containsProperty(property: Int): Boolean =
    properties and property != 0

fun BluetoothGattCharacteristic.printProperties(): String = mutableListOf<String>().apply {
    if (isReadable()) add("READABLE")
    if (isWritable()) add("WRITABLE")
    if (isWritableWithoutResponse()) add("WRITABLE WITHOUT RESPONSE")
    if (isIndicatable()) add("INDICATABLE")
    if (isNotifiable()) add("NOTIFIABLE")
    if (isEmpty()) add("EMPTY")
}.joinToString()

fun BluetoothGatt.printGattTable() {
    if (services.isEmpty()) {
        Timber.i("No service and characteristic available, call discoverServices() first?")
        return
    }
    services.forEach { service ->
        val characteristicsTable = service.characteristics.joinToString(
            separator = "\n|--", prefix = "|--"
        ) { char ->
            var description = "${char.uuid}: ${char.printProperties()}"
            if (char.descriptors.isNotEmpty()) {
                description += "\n" + char.descriptors.joinToString(
                    separator = "\n|------", prefix = "|------"
                ) { descriptor ->
                    "${descriptor.uuid}: ${descriptor.printProperties()}"
                }
            }
            description
        }
        Timber.d("Service ${service.uuid}\nCharacteristics:\n$characteristicsTable")
    }
}

/**
 * Kotlinx serialization of generic map
 */

val prettyJson by lazy { Json { prettyPrint = true } }

fun Array<*>.toJsonArray(): JsonArray {
    val array = mutableListOf<JsonElement>()
    this.forEach { array.add(it.toJsonElement()) }
    return JsonArray(array)
}

fun List<*>.toJsonArray(): JsonArray {
    val array = mutableListOf<JsonElement>()
    this.forEach { array.add(it.toJsonElement()) }
    return JsonArray(array)
}

fun Map<*, *>.toJsonObject(): JsonObject {
    val map = mutableMapOf<String, JsonElement>()
    this.forEach {
        val keyStr = it.key.toString()
        if (map.containsKey(keyStr)) {
            throw Exception("Encoding duplicate keys $keyStr")
        }
        map[keyStr] = it.value.toJsonElement()
    }
    return JsonObject(map)
}

@OptIn(ExperimentalUnsignedTypes::class)
fun Any?.toJsonElement(): JsonElement {
    return when (this) {
        is Number -> JsonPrimitive(this)
        is Boolean -> JsonPrimitive(this)
        is String -> JsonPrimitive(this)
        is Array<*> -> this.toJsonArray()
        is List<*> -> this.toJsonArray()
        is Map<*, *> -> this.toJsonObject()
        is UByteArray -> this.toHexString().toJsonElement()
        is UByte -> ubyteArrayOf(this).toJsonElement()
        is JsonElement -> this
        null -> JsonNull
        else -> {
            throw Exception("Can not encode value ${this::class} to JSON")
        }
    }
}
