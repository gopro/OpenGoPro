package gopro

import domain.api.IOperationMarshaller
import entity.constants.StatusId
import extensions.toBoolean
import operation.queries.StatusFacade

@OptIn(ExperimentalUnsignedTypes::class)
class StatusesContainer internal constructor(marshaller: IOperationMarshaller) {
    val isBusy = StatusFacade(StatusId.IS_BUSY, marshaller) { it.last().toBoolean() }
    val isEncoding = StatusFacade(StatusId.IS_ENCODING, marshaller) { it.last().toBoolean() }
}