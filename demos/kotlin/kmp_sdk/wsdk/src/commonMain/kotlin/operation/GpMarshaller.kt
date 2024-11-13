package operation

import co.touchlab.kermit.Logger
import domain.api.IOperation
import domain.api.IOperationMarshaller
import domain.api.StrategyBuilder
import domain.api.operationStrategy
import domain.communicator.ICommunicator
import domain.gopro.IGpDescriptor
import entity.communicator.CommunicationType
import entity.exceptions.OperationUnsupportedForCommunicator
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.first

private val logger = Logger.withTag("GpMarshaller")
private const val TRACE_LOG = true

// TODO configure and inject
private fun traceLog(message: String) = if (TRACE_LOG) logger.d(message) else {
}

// TODO how to inject default strategy since lambdas can't have generic types
internal class GpMarshaller(private val gopro: IGpDescriptor) : IOperationMarshaller {
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

        logger.i("Setting up GoPro ${gopro.serialId} communicator: ${communicator.communicationType}")
        communicator.setup()

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
            traceLog("Waiting for camera to be ready before executing ${operation.debugId}.")
            gopro.isReady.filter { it }.first()
            traceLog("Camera is ready. Executing ${operation.debugId}")
        }
        // Ready to go, now perform the operation
        val targetCommunicator = normalizedStrategy.useCommunicator(
            operation,
            gopro
        )
        val response = communicatorMap[targetCommunicator]?.let { communicator ->
            operation.execute(communicator)
        } ?: throw OperationUnsupportedForCommunicator(operation.debugId, targetCommunicator)
        // Should we wait for encoding to stop before returning?
        if ((gopro.isEncoding.value) &&
            (normalizedStrategy.shouldWaitForEncodingStop(operation, gopro))
        ) {
            traceLog("Waiting for encoding to stop before completing ${operation.debugId}.")
            gopro.isEncoding.filter { !it }.first()
            traceLog("Encoding has stopped. Completing ${operation.debugId}.")
        }
        return response
    }
}