/* FakeWifiApi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

import com.gopro.open_gopro.domain.network.IWifiApi
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class FakeWifiApi(override val dispatcher: CoroutineDispatcher) : IWifiApi {
  override suspend fun setup() {
    TODO("Not yet implemented")
  }

  override suspend fun scanForSsid(): Result<Flow<String>> {
    TODO("Not yet implemented")
  }

  override suspend fun connect(ssid: String, password: String): Result<Unit> {
    TODO("Not yet implemented")
  }

  override suspend fun disconnect(ssid: String): Result<Unit> {
    TODO("Not yet implemented")
  }

  override fun receiveDisconnects(): Flow<String> = flow {}
}
