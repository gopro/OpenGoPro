package di

import WsdkAppContext
import connector.CameraConnector
import connector.GpBleConnector
import connector.GpDnsConnector
import connector.GpWifiConnector
import domain.connector.ICameraConnector
import domain.gopro.IGoProFactory
import domain.network.IBleApi
import domain.network.IHttpApi
import gopro.GoProFactory
import kotlinx.coroutines.CoroutineDispatcher
import network.KableBle
import network.KtorHttp
import org.koin.dsl.module

internal fun buildPackageModules(dispatcher: CoroutineDispatcher, appContext: WsdkAppContext) =
    module {
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
                GpDnsConnector(get(), get()),
            )
        }
        // Top level facade
        single<IGoProFactory> {
            GoProFactory(get(), get(), get(), get(), get())
        }
    }