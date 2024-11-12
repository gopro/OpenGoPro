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
import io.ktor.client.HttpClient
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import network.KableBle
import network.KtorHttp
import org.koin.dsl.module

val packageModule = module {
    // TODO is this correct? Should it be named?
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
    single<GoProFacadeFactory> { GoProFacadeFactory(get(), get(), get(), get(), get(), get(), get()) }
}