/* FakeCameraConnector.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package fakes

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import com.gopro.open_gopro.domain.connector.ICameraConnector
import kotlinx.coroutines.flow.Flow

internal class FakeCameraConnector : ICameraConnector {
  override suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult> {
    TODO("Not yet implemented")
  }

  override suspend fun connect(
      target: ScanResult,
      connectionRequestContext: ConnectionRequestContext?
  ): Result<ConnectionDescriptor> {
    TODO("Not yet implemented")
  }
}
