/* IGoProFacadeFactory.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.domain.gopro

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.gopro.GoPro

internal interface IGoProFactory {
  suspend fun getGoPro(id: GoProId): Result<GoPro>

  suspend fun storeConnection(connection: ConnectionDescriptor)
}
