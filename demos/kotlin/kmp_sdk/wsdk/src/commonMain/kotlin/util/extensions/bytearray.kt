package util.extensions

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
    (3 downTo 0).map {
        (this shr (it * Byte.SIZE_BITS)).toUByte()
    }.toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
internal fun UByteArray.toTlvMap(): Map<UByte, UByteArray> {
    var buf = this.toList()
    val map = mutableMapOf<UByte, UByteArray>()
    while (buf.isNotEmpty()) {
        val t = buf.first()
        buf = buf.drop(1)
        val l = buf.first().toInt()
        buf = buf.drop(1)
        val v = buf.slice(0..<l).toUByteArray()
        map[t] = v
        buf = buf.drop(l)
    }
    return map
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun List<UByte>.toTlvMap(): Map<UByte, UByteArray> = this.toUByteArray().toTlvMap()

@OptIn(ExperimentalStdlibApi::class, ExperimentalUnsignedTypes::class)
internal fun UByteArray.toPrettyHexString(): String =
    this.joinToString(separator = " ") {
        it.toHexString()
    }

@OptIn(ExperimentalUnsignedTypes::class)
internal fun ByteArray.toPrettyHexString(): String = this.toUByteArray().toPrettyHexString()

internal fun Boolean.toInt(): Int = if (this) 1 else 0
internal fun Int.toBoolean(): Boolean = this != 0