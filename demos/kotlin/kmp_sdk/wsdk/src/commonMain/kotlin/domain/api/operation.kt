package domain.api

import co.touchlab.kermit.Logger
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.ICommunicator
import domain.gopro.IGpDescriptor
import entity.communicator.CommunicationType
import entity.exceptions.OperationUnsupportedForCommunicator
import extensions.bleIfAvailable
import extensions.prettyPrintResult

interface IOperation<T : Any> {
    val debugId: String
    suspend fun execute(communicator: ICommunicator<*>): Result<T>
}

internal abstract class BaseOperation<T : Any>(final override val debugId: String) : IOperation<T> {
    protected val logger = Logger.withTag(debugId)

    open suspend fun execute(communicator: BleCommunicator): Result<T> =
        throw OperationUnsupportedForCommunicator(debugId, communicator.communicationType)

    open suspend fun execute(communicator: HttpCommunicator): Result<T> =
        throw OperationUnsupportedForCommunicator(debugId, communicator.communicationType)

    final override suspend fun execute(communicator: ICommunicator<*>): Result<T> {
        logger.i("Executing $debugId with ${communicator.communicationType} communicator")
        val result = when (communicator) {
            is BleCommunicator -> execute(communicator)
            is HttpCommunicator -> execute(communicator)
            else -> {
                throw Exception("Should be impossible to get an unsupported communicator.")
            }
        }
        logger.i("$debugId finished with result ==> ${prettyPrintResult(result)}")
        return result
    }
}

interface IOperationMarshaller {
    suspend fun <T : Any, O : IOperation<T>> marshal(
        operation: O, strategy: (StrategyBuilder<T, O>.() -> Unit)? = null
    ): Result<T>

    suspend fun bindCommunicator(communicator: ICommunicator<*>): Boolean
    fun removeCommunicator(communicator: ICommunicator<*>)
    val communicators: List<CommunicationType>
}

interface IOperationStrategy<T : Any, O : IOperation<T>> {
    fun isFastpass(operation: O, device: IGpDescriptor): Boolean
    fun useCommunicator(operation: O, device: IGpDescriptor): CommunicationType
    fun shouldWaitForEncodingStop(operation: O, device: IGpDescriptor): Boolean
}

@DslMarker
annotation class StrategyDsl

@StrategyDsl
class StrategyBuilder<T : Any, O : IOperation<T>> {
    private var communicatorStrategy: (O, IGpDescriptor) -> CommunicationType =
        { _, device -> device.communicators.run { bleIfAvailable() ?: first() } }
    private var fastpassStrategy: (O, IGpDescriptor) -> Boolean = { _, _ -> false }
    private var waitEncodingStopStrategy: (O, IGpDescriptor) -> Boolean = { _, _ -> false }

    fun build() = object : IOperationStrategy<T, O> {
        override fun isFastpass(operation: O, device: IGpDescriptor): Boolean =
            fastpassStrategy(operation, device)

        override fun useCommunicator(operation: O, device: IGpDescriptor): CommunicationType =
            communicatorStrategy(operation, device)

        override fun shouldWaitForEncodingStop(
            operation: O,
            device: IGpDescriptor
        ): Boolean =
            waitEncodingStopStrategy(operation, device)

    }

    fun useCommunicator(strategy: (O, IGpDescriptor) -> CommunicationType) {
        this.communicatorStrategy = strategy
    }

    fun isFastpass(strategy: (O, IGpDescriptor) -> Boolean) {
        this.fastpassStrategy = strategy
    }

    fun waitForEncodingStop(strategy: (O, IGpDescriptor) -> Boolean) {
        this.waitEncodingStopStrategy = strategy
    }
}

internal fun <T : Any, O : IOperation<T>> operationStrategy(initializer: StrategyBuilder<T, O>.() -> Unit): IOperationStrategy<T, O> {
    return StrategyBuilder<T, O>().apply(initializer).build()
}