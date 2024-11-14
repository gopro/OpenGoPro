package di

import WsdkAppContext
import connector.GpBleConnector
import connector.GpDnsConnector
import connector.GpWifiConnector
import domain.connector.ICameraConnector
import domain.gopro.IGoProFacadeFactory
import domain.network.IBleApi
import domain.network.IHttpApi
import connector.CameraConnector
import gopro.GoProFacadeFactory
import kotlinx.coroutines.CoroutineDispatcher
import network.KableBle
import network.KtorHttp
import org.koin.dsl.module

internal fun buildPackageModules(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) = module {
    single<CoroutineDispatcher> { dispatcher }

    includes(buildWsdkPlatformModules(appContext))

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