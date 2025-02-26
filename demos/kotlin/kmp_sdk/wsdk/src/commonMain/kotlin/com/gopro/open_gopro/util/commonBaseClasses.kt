/* commonBaseClasses.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.util

import co.touchlab.kermit.Logger
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope

internal interface IGpCommonBase {
  val logger: Logger
  val scope: CoroutineScope?

  fun traceLog(message: String)
}

// TODO configure and inject logger
internal class GpCommonBase(
    debugName: String,
    dispatcher: CoroutineDispatcher? = null,
    private val shouldEnableTraceLog: Boolean = false,
) : IGpCommonBase {
  override val logger = Logger.withTag(debugName)

  private val coroutineExceptionHandler = CoroutineExceptionHandler { _, throwable ->
    logger.e("Caught exception in coroutine:", throwable)
  }

  override val scope = dispatcher?.let { CoroutineScope(it + coroutineExceptionHandler) }

  override fun traceLog(message: String) = if (shouldEnableTraceLog) logger.d(message) else {}
}
