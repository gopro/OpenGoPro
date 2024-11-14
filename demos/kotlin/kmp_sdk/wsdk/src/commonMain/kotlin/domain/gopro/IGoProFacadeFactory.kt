package domain.gopro

import entity.connector.ConnectionDescriptor
import gopro.GoPro


interface IGoProFactory {
    suspend fun getGoPro(serialId: String): GoPro
    suspend fun storeConnection(connection: ConnectionDescriptor)
}