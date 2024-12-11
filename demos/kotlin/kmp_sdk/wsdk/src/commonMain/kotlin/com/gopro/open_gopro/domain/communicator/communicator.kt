package com.gopro.open_gopro.domain.communicator

import com.gopro.open_gopro.entity.communicator.CommunicationType
import com.gopro.open_gopro.entity.connector.ConnectionDescriptor

// Note! This is theoretically a source of instability as any new communicator causes changes in
// all operations. These would ideally be abstract.
// However this is accepted as this change is rare and allows concise of definition
// of operations.
// Also these can't be injected (at least not usefully) since they are too different

internal sealed class ICommunicator<T : ConnectionDescriptor> {
    abstract val connection: T
    abstract val communicationType: CommunicationType
    val id get() = connection.id
}