package di

import Wsdk
import domain.connector.ICameraConnector
import domain.gopro.IGoProFactory
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildWsdkModule(): Module {
    return module {
        single<ICameraConnector> { Wsdk.getCameraConnector() }
        single<IGoProFactory> { Wsdk.getGoProFactory() }
    }
}