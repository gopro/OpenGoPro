package di

import AppContext
import connector.GpBleConnector
import connector.GpDnsConnector
import connector.GpWifiConnector
import domain.network.IBleApi
import domain.network.IHttpApi
import entity.connector.ICameraConnector
import gopro.CameraConnector
import gopro.GoProFacadeFactory
import gopro.IGoProFacadeFactory
import kotlinx.coroutines.CoroutineDispatcher
import network.KableBle
import network.KtorHttp
import org.koin.dsl.module

fun buildPackageModules(dispatcher: CoroutineDispatcher, appContext: AppContext) = module {
    includes(buildWsdkPlatformModules(appContext))

    single<CoroutineDispatcher> { dispatcher }

    // Network ConnectorFactory and communicator APIs
    single<IBleApi> { KableBle(get()) }
    single<IHttpApi> { KtorHttp() }

    // Network ConnectorFactory and communicator factories
    single<ICameraConnector> {
        CameraConnector(
            GpBleConnector(get()),
            GpWifiConnector(get()),
            GpDnsConnector(get(), get())
        )
    }
    // Top level facade
    single<IGoProFacadeFactory> {
        GoProFacadeFactory(
            get(),
            get(),
            get(),
            get(),
            get(),
            get(),
            get()
        )
    }
}