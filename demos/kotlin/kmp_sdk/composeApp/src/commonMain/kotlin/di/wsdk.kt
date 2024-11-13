package di

import AppContext
import Wsdk
import entity.connector.ICameraConnector
import gopro.IGoProFacadeFactory
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildWsdkModule(appContext: AppContext): Module {
    Wsdk.init(Dispatchers.IO, appContext)
    return module {
        single<ICameraConnector> { Wsdk.getCameraConnector() }
        single<IGoProFacadeFactory> { Wsdk.getGoProFacadeFactory() }
    }
}