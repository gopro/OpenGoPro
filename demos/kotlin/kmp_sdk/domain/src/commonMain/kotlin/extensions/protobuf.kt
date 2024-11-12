package extensions

import entity.exceptions.CameraInternalError
import open_gopro.EnumResultGeneric
import open_gopro.ResponseGeneric
import pbandk.decodeFromByteArray

fun Result<ByteArray>.mapFromGenericProtoResponseToResult(): Result<Unit> =
    this.map {
        ResponseGeneric.decodeFromByteArray(it).result.run {
            if (this == EnumResultGeneric.RESULT_SUCCESS) {
                Result.success(Unit)
            } else {
                Result.failure(CameraInternalError(this.toString()))
            }
        }
    }

fun EnumResultGeneric.isOk(): Boolean = (this == EnumResultGeneric.RESULT_SUCCESS)