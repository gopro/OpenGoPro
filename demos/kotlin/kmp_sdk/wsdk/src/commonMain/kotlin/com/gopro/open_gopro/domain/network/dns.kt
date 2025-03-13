/* dns.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.network

import kotlinx.coroutines.flow.Flow

internal data class DnsScanResult(val ipAddress: String, val serviceName: String)

internal interface IDnsApi {
  suspend fun scan(serviceType: String): Result<Flow<DnsScanResult>>
}
