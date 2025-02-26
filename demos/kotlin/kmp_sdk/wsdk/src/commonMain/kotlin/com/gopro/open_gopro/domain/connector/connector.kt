/* connector.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.connector

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.ConnectionRequestContext
import com.gopro.open_gopro.NetworkType
import com.gopro.open_gopro.ScanResult
import kotlinx.coroutines.flow.Flow

internal interface ICameraConnector {
  suspend fun discover(vararg networkTypes: NetworkType): Flow<ScanResult>

  suspend fun connect(
      target: ScanResult,
      connectionRequestContext: ConnectionRequestContext? = null
  ): Result<ConnectionDescriptor>
}

internal interface IConnector<S : ScanResult, C : ConnectionDescriptor> {
  val networkType: NetworkType

  suspend fun scan(): Result<Flow<S>>

  suspend fun connect(target: S, request: ConnectionRequestContext? = null): Result<C>

  suspend fun disconnect(connection: C): Result<Unit>
}
