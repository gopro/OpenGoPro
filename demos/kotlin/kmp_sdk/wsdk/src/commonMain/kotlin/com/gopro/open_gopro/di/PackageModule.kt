package com.gopro.open_gopro.di

import com.gopro.open_gopro.WsdkAppContext
import com.gopro.open_gopro.connector.CameraConnector
import com.gopro.open_gopro.connector.GpBleConnector
import com.gopro.open_gopro.connector.GpDnsConnector
import com.gopro.open_gopro.connector.GpWifiConnector
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.domain.network.IHttpApi
import com.gopro.open_gopro.gopro.GoProFactory
import kotlinx.coroutines.CoroutineDispatcher
import com.gopro.open_gopro.network.KableBle
import com.gopro.open_gopro.network.KtorHttp
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