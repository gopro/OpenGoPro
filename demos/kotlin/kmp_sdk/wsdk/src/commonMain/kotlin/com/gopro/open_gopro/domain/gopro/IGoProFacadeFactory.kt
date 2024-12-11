package com.gopro.open_gopro.domain.gopro

import com.gopro.open_gopro.entity.connector.ConnectionDescriptor
import com.gopro.open_gopro.entity.connector.GoProId
import com.gopro.open_gopro.gopro.GoPro


internal interface IGoProFactory {
    suspend fun getGoPro(id: GoProId): GoPro
    suspend fun storeConnection(connection: ConnectionDescriptor)
}