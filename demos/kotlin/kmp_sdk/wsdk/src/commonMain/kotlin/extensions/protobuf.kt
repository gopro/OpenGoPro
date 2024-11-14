package extensions

import entity.exceptions.CameraInternalError
import entity.operation.proto.EnumResultGeneric
import entity.operation.proto.ResponseGeneric
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