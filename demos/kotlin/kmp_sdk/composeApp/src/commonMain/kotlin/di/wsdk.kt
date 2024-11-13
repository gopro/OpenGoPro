package di

import Wsdk
import entity.connector.ICameraConnector
import gopro.IGoProFacadeFactory
import org.koin.dsl.KoinAppDeclaration
import org.koin.dsl.module

fun buildWsdkModule(config: KoinAppDeclaration? = null) =
    module {
        single<ICameraConnector> { Wsdk.getCameraConnector(config) }
        single<IGoProFacadeFactory> { Wsdk.getGoProFacadeFactory(config) }
    }