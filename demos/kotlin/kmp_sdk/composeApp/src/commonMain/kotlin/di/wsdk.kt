package di

import Wsdk
import entity.connector.ICameraConnector
import gopro.CameraConnector
import gopro.GoProFacadeFactory
import org.koin.dsl.KoinAppDeclaration
import org.koin.dsl.module

fun buildWsdkModule(config: KoinAppDeclaration? = null) =
    module {
        single<ICameraConnector> { Wsdk.getCameraConnector(config) }
        single<GoProFacadeFactory> { Wsdk.getGoProFacadeFactory(config) }
    }