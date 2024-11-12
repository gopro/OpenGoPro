package extensions

fun Byte.toBoolean(): Boolean = this.toInt() != 0
fun UByte.toBoolean(): Boolean = this.toByte().toBoolean()
fun Boolean.toUByte(): UByte = if (this) 1U else 0U

@OptIn(ExperimentalUnsignedTypes::class)
fun UByteArray.decodeToString(): String = this.toByteArray().decodeToString()

@OptIn(ExperimentalUnsignedTypes::class)
fun String.encodeToUByteArray(): UByteArray = this.encodeToByteArray().toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
fun UByte.toUByteArray(): UByteArray = ubyteArrayOf(this)

@OptIn(ExperimentalUnsignedTypes::class)
fun List<Int>.toUByteArray(): UByteArray = this.map { it.toUByte() }.toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
fun UInt.toUByteArray(): UByteArray =
    (3 downTo 0).map {
        (this shr (it * Byte.SIZE_BITS)).toUByte()
    }.toUByteArray()

@OptIn(ExperimentalUnsignedTypes::class)
fun UByteArray.toTlvMap(): Map<UByte, UByteArray> {
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
fun List<UByte>.toTlvMap(): Map<UByte, UByteArray> = this.toUByteArray().toTlvMap()

@OptIn(ExperimentalStdlibApi::class, ExperimentalUnsignedTypes::class)
fun UByteArray.toPrettyHexString(): String =
    this.joinToString(separator = " ") {
        it.toHexString()
    }

@OptIn(ExperimentalUnsignedTypes::class)
fun ByteArray.toPrettyHexString(): String = this.toUByteArray().toPrettyHexString()

fun Boolean.toInt(): Int = if (this) 1 else 0
fun Int.toBoolean(): Boolean = this != 0