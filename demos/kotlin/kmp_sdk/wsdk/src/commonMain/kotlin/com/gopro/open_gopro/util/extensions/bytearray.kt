/* bytearray.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util.extensions

internal fun Byte.toBoolean(): Boolean = this.toInt() != 0

internal fun UByte.toBoolean(): Boolean = this.toByte().toBoolean()

internal fun Boolean.toUByte(): UByte = if (this) 1U else 0U

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.decodeToString(): String = this.toByteArray().decodeToString()

@OptIn(ExperimentalUnsignedTypes::class)
internal fun String.encodeToUByteArray(): UByteArray = this.encodeToByteArray().toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByte.toUByteArray(): UByteArray = ubyteArrayOf(this)

@OptIn(ExperimentalUnsignedTypes::class)
internal fun List<Int>.toUByteArray(): UByteArray = this.map { it.toUByte() }.toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UInt.toUByteArray(): UByteArray =
    (3 downTo 0).map { (this shr (it * Byte.SIZE_BITS)).toUByte() }.toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.toTlvMap(): Map<UByte, List<UByteArray>> {
  var buf = this.toList()
  val map = mutableMapOf<UByte, MutableList<UByteArray>>()
  while (buf.isNotEmpty()) {
    val t = buf.first()
    buf = buf.drop(1)
    val l = buf.first().toInt()
    buf = buf.drop(1)
    val v = buf.slice(0..<l).toUByteArray()
    map.getOrPut(t) { mutableListOf() } += v
    buf = buf.drop(l)
  }
  return map
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun List<UByte>.toTlvMap(): Map<UByte, List<UByteArray>> = this.toUByteArray().toTlvMap()

@OptIn(ExperimentalStdlibApi::class, ExperimentalUnsignedTypes::class)
internal fun UByteArray.toPrettyHexString(): String =
    this.joinToString(separator = " ") { it.toHexString() }

@OptIn(ExperimentalUnsignedTypes::class)
internal fun ByteArray.toPrettyHexString(): String = this.toUByteArray().toPrettyHexString()

internal fun Boolean.toInt(): Int = if (this) 1 else 0

internal fun Int.toBoolean(): Boolean = this != 0

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.asInt64UB(): ULong {
  if (this.size != 4) {
    throw Exception("Array must be exactly 4 bytes to convert to Int64UB")
  }
  var value = 0UL
  value += this[0].toULong()
  value += this[1].toULong().shl(8)
  value += this[2].toULong().shl(16)
  value += this[3].toULong().shl(24)
  return value
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun ULong.toUByteArray(): UByteArray {
  val mask = 0xFFUL
  var value = ubyteArrayOf()
  value += this.and(mask).toUByte()
  value += this.and(mask.shl(8)).shr(8).toUByte()
  value += this.and(mask.shl(16)).shr(16).toUByte()
  value += this.and(mask.shl(24)).shr(24).toUByte()
  return value
}
