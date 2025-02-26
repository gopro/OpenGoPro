/* GpMarshaller.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations

import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.domain.api.IOperation
import com.gopro.open_gopro.domain.api.IOperationMarshaller
import com.gopro.open_gopro.domain.api.StrategyBuilder
import com.gopro.open_gopro.domain.api.operationStrategy
import com.gopro.open_gopro.domain.communicator.ICommunicator
import com.gopro.open_gopro.gopro.IGpDescriptor
import com.gopro.open_gopro.util.GpCommonBase
import com.gopro.open_gopro.util.IGpCommonBase
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.first

internal class GpMarshaller(private val gopro: IGpDescriptor) :
    IOperationMarshaller, IGpCommonBase by GpCommonBase("GpMarshaller") {

  private val communicatorMap = mutableMapOf<CommunicationType, ICommunicator<*>>()

  override val communicators: List<CommunicationType>
    get() = communicatorMap.keys.toList()

  override fun removeCommunicator(communicator: ICommunicator<*>) {
    if (communicatorMap.containsKey(communicator.communicationType)) return

    logger.d("Removing communicator: ${communicator.communicationType}")
    communicatorMap.remove(communicator.communicationType)
  }

  override suspend fun bindCommunicator(communicator: ICommunicator<*>): Boolean {
    // TODO This assumes that we have no reason to update a communicator.
    // This will need to be investigated when testing reconnections.
    if (communicatorMap.containsKey(communicator.communicationType)) return false

    logger.i("Setting up GoPro ${gopro.id} communicator: ${communicator.communicationType}")

    logger.d("Binding communicator: ${communicator.communicationType}")
    communicatorMap[communicator.communicationType] = communicator
    return true
  }

  override suspend fun <T : Any, O : IOperation<T>> marshal(
      operation: O,
      strategy: (StrategyBuilder<T, O>.() -> Unit)?
  ): Result<T> {
    // Use default strategy if none was passed
    val normalizedStrategy =
        strategy?.let { operationStrategy(it) } ?: StrategyBuilder<T, O>().build()
    // If not ready and not fastpass, wait for busy
    if ((!gopro.isReady.value) && !(normalizedStrategy.isFastpass(operation, gopro))) {
      logger.d("Waiting for camera to be ready before executing ${operation.debugId}.")
      gopro.isReady.filter { it }.first()
      logger.d("Camera is ready. Executing ${operation.debugId}")
    }
    // Ready to go, now perform the operation
    val targetCommunicator = normalizedStrategy.useCommunicator(operation, gopro)
    val response =
        communicatorMap[targetCommunicator]?.let { communicator -> operation.execute(communicator) }
            ?: throw OperationUnsupportedForCommunicator(operation.debugId, targetCommunicator)
    // Should we wait for encoding to stop before returning?
    if ((gopro.isEncoding.value) &&
        (normalizedStrategy.shouldWaitForEncodingStop(operation, gopro))) {
      logger.d("Waiting for encoding to stop before completing ${operation.debugId}.")
      gopro.isEncoding.filter { !it }.first()
      logger.d("Encoding has stopped. Completing ${operation.debugId}.")
    }
    return response
  }
}
