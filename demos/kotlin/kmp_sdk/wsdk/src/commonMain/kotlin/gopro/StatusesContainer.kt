package gopro

import domain.api.IOperationMarshaller
import domain.queries.Status
import entity.queries.StatusId
import extensions.toBoolean

@OptIn(ExperimentalUnsignedTypes::class)
private fun toBoolean(data: UByteArray): Boolean = data.last().toBoolean()

/**
 * Container for all per-status-ID wrappers
 *
 * Note! This is a very small subset of the supported statuses. TODO these need to be automatically
 * generated.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html)
 *
 * @param marshaller
 */
@OptIn(ExperimentalUnsignedTypes::class)
class StatusesContainer internal constructor(marshaller: IOperationMarshaller) {
    /**
     * Is the camera busy?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8)
     */
    val isBusy = Status(StatusId.IS_BUSY, marshaller, ::toBoolean)

    /**
     * Is the camera currently encoding?
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10)
     */
    val isEncoding = Status(StatusId.IS_ENCODING, marshaller, ::toBoolean)
}