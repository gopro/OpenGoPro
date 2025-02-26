/* protobuf.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util.extensions

import com.gopro.open_gopro.gopro.CameraInternalError
import com.gopro.open_gopro.operations.EnumResultGeneric
import com.gopro.open_gopro.operations.ResponseGeneric
import pbandk.decodeFromByteArray

internal fun Result<ByteArray>.mapFromGenericProtoResponseToResult(): Result<Unit> =
    this.map {
      ResponseGeneric.decodeFromByteArray(it).result.run {
        if (this == EnumResultGeneric.RESULT_SUCCESS) {
          Result.success(Unit)
        } else {
          Result.failure(CameraInternalError(this.toString()))
        }
      }
    }

internal fun EnumResultGeneric.isOk(): Boolean = (this == EnumResultGeneric.RESULT_SUCCESS)
