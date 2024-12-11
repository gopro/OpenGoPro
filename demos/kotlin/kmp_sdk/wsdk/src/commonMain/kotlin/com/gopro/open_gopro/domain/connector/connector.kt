package com.gopro.open_gopro.domain.connector

import com.gopro.open_gopro.entity.connector.ConnectionDescriptor
import com.gopro.open_gopro.entity.connector.ConnectionRequestContext
import com.gopro.open_gopro.entity.connector.NetworkType
import com.gopro.open_gopro.entity.connector.ScanResult
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