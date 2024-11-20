package util

import co.touchlab.kermit.Logger
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope

internal interface IGpGenericBase {
    val logger: Logger
    val scope: CoroutineScope?
    fun traceLog(message: String)
}

// TODO configure and inject logger
internal class GpGenericBase(
    debugName: String,
    dispatcher: CoroutineDispatcher? = null,
    private val shouldEnableTraceLog: Boolean = false,
) : IGpGenericBase {
    override val logger = Logger.withTag(debugName)

    private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
        logger.e("Caught exception in coroutine:", throwable)
    }

    override val scope = dispatcher?.let { CoroutineScope(it + coroutineExceptionHandler) }

    override fun traceLog(message: String) = if (shouldEnableTraceLog) logger.d(message) else {
    }
}