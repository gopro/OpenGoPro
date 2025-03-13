/* Statuses.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.QueryId
import com.gopro.open_gopro.operations.StatusId
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart

/**
 * A per-status ID wrapper to perform all status queries
 *
 * @param T Status data type
 * @property statusId Status ID
 * @property marshaller operation marshaller to marshal the queries
 * @property fromUByteArray status value-from-UByte transformer
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/statuses.html)
 */
@OptIn(ExperimentalUnsignedTypes::class)
class Status<T : Any>
internal constructor(
    private val statusId: StatusId,
    private val marshaller: IOperationMarshaller,
    private val fromUByteArray: (UByteArray) -> T
) {
  private inner class GetStatusValue : BaseOperation<T>("Get Status Value::${statusId.name}") {
    override suspend fun execute(communicator: BleCommunicator): Result<T> =
        communicator.executeQuery(QueryId.GET_STATUS_VALUES, statusId).map { fromUByteArray(it) }
  }

  private inner class RegisterForStatusValueUpdates :
      BaseOperation<Flow<T>>("Register Status Value Updates::${statusId.name}") {

    override suspend fun execute(communicator: BleCommunicator): Result<Flow<T>> {
      // Send initial query OTA to register and store current value for later returning
      val currentValue =
          communicator
              .executeQuery(QueryId.REGISTER_STATUS_VALUE_UPDATES, statusId)
              .fold(
                  onFailure = {
                    return Result.failure(it)
                  },
                  onSuccess = { fromUByteArray(it) },
              )

      // Now actually register to receive notifications
      return communicator
          .registerUpdate(ResponseId.QueryStatus(QueryId.ASYNC_STATUS_VALUE_NOTIFICATION, statusId))
          .map { flow -> flow.map { fromUByteArray(it.payload) }.onStart { emit(currentValue) } }
    }
  }

  /**
   * Get the current status value
   *
   * @return current status value
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/query.html#get-status-values)
   */
  suspend fun getValue(): Result<T> = marshaller.marshal(GetStatusValue())

  /**
   * Register for status value updates
   *
   * @return continuous flow of status value updates
   */
  suspend fun registerValueUpdate(): Result<Flow<T>> =
      // TODO Can we always allow fastpass here? It's needed to set up initial state querying.
      // If not, need to add initializing in descriptor.
      marshaller.marshal(RegisterForStatusValueUpdates()) {
        isFastpass { _, _ -> true }
        useCommunicator { _, _ -> CommunicationType.BLE }
      }

  // TODO other queries
}
