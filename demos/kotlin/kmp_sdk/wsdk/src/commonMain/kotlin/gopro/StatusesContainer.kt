package gopro

import domain.api.IOperationMarshaller
import entity.constants.StatusId
import extensions.toBoolean
import operation.queries.Status

@OptIn(ExperimentalUnsignedTypes::class)
class StatusesContainer internal constructor(marshaller: IOperationMarshaller) {
    val isBusy = Status(StatusId.IS_BUSY, marshaller) { it.last().toBoolean() }
    val isEncoding = Status(StatusId.IS_ENCODING, marshaller) { it.last().toBoolean() }
}