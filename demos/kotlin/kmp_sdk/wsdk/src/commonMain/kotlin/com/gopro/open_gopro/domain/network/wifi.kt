/* wifi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.network

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow

internal interface IWifiApi {
  val dispatcher: CoroutineDispatcher

  suspend fun setup()

  suspend fun scanForSsid(): Result<Flow<String>>

  suspend fun connect(ssid: String, password: String): Result<Unit>

  suspend fun disconnect(ssid: String): Result<Unit>

  fun receiveDisconnects(): Flow<String>
}
