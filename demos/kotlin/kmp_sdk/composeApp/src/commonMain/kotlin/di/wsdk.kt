package di

import Wsdk
import entity.connector.ICameraConnector
import gopro.IGoProFacadeFactory
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildWsdkModule(): Module {
    return module {
        single<ICameraConnector> { Wsdk.getCameraConnector() }
        single<IGoProFacadeFactory> { Wsdk.getGoProFacadeFactory() }
    }
}