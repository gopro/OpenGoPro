/* strings.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util.extensions

// It's not really an extension...
@OptIn(ExperimentalUnsignedTypes::class)
internal fun prettyPrintResult(result: Result<Any>): String {
  if (result.isFailure) return result.exceptionOrNull().toString()

  return "Success: " +
      result.getOrThrow().let { value ->
        (value as? Unit)?.let { "" }
            ?: (value as? Int)?.toString()
            ?: (value as? Float)?.toString()
            ?: (value as? Long)?.toString()
            ?: (value as? ByteArray)?.toPrettyHexString()
            ?: (value as? UByteArray)?.toPrettyHexString()
            ?: (value as? String)
            ?: value.toString()
      }
}
