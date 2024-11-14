package domain.gopro

import entity.connector.ConnectionDescriptor
import entity.connector.GoProId
import gopro.GoPro


internal interface IGoProFactory {
    suspend fun getGoPro(id: GoProId): GoPro
    suspend fun storeConnection(connection: ConnectionDescriptor)
}