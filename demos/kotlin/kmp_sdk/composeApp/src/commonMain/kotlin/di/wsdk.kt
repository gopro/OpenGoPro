package di

import Wsdk
import entity.connector.ICameraConnector
import gopro.IGoProFactory
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildWsdkModule(): Module {
    return module {
        single<ICameraConnector> { Wsdk.getCameraConnector() }
        single<IGoProFactory> { Wsdk.getGoProFactory() }
    }
}