package di

import connector.GpBleConnector
import connector.GpDnsConnector
import connector.GpWifiConnector
import domain.network.IBleApi
import domain.network.IHttpApi
import domain.network.IHttpClientProvider
import entity.connector.ICameraConnector
import gopro.CameraConnector
import gopro.GoProFacadeFactory
import gopro.IGoProFacadeFactory
import io.ktor.client.HttpClient
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import network.KableBle
import network.KtorHttp
import org.koin.dsl.module

internal val packageModule = module {
    // TODO should this be configurable by the client?
    single<CoroutineDispatcher> { Dispatchers.IO }

    includes(buildWsdkPlatformModules())

    // Network ConnectorFactory and communicator APIs
    single<IBleApi> { KableBle(get()) }
    single<IHttpApi> { KtorHttp() }

    // Network ConnectorFactory and communicator factories
    single<ICameraConnector> {
        CameraConnector(
            GpBleConnector(get(), get()),
            GpWifiConnector(get(), get()),
            GpDnsConnector(get(), get())
        )
    }
    // Top level facade
    single<IGoProFacadeFactory> { GoProFacadeFactory(get(), get(), get(), get(), get(), get(), get()) }
}