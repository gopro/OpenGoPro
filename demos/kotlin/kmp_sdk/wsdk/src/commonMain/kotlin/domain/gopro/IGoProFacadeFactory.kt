package domain.gopro

import entity.connector.ConnectionDescriptor
import gopro.GoProFacade


interface IGoProFacadeFactory {
    suspend fun getGoProFacade(serialId: String): GoProFacade
    suspend fun storeConnection(connection: ConnectionDescriptor)
}