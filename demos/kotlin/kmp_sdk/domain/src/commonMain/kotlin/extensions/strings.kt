package extensions

import kotlinx.coroutines.flow.Flow

// It's not really an extension...
@OptIn(ExperimentalUnsignedTypes::class)
fun prettyPrintResult(result: Result<Any>): String {
    if (result.isFailure) return result.exceptionOrNull().toString()

    return "Success: " + result.getOrThrow().let { value ->
        (value as? Unit)?.let { "" } ?:
        (value as? Int)?.toString() ?:
        (value as? Float)?.toString() ?:
        (value as? Long)?.toString() ?:
        (value as? ByteArray)?.toPrettyHexString() ?:
        (value as? UByteArray)?.toPrettyHexString() ?:
        (value as? String) ?:
        value.toString()
    }
}