package com.gopro.open_gopro.util.extensions

import com.gopro.open_gopro.exceptions.CameraInternalError
import com.gopro.open_gopro.entity.operation.proto.EnumResultGeneric
import com.gopro.open_gopro.entity.operation.proto.ResponseGeneric
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