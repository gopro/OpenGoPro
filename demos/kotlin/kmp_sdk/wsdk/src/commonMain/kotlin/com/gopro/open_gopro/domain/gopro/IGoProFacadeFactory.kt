package com.gopro.open_gopro.domain.gopro

import com.gopro.open_gopro.ConnectionDescriptor
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.gopro.GoPro


internal interface IGoProFactory {
    suspend fun getGoPro(id: GoProId): GoPro
    suspend fun storeConnection(connection: ConnectionDescriptor)
}