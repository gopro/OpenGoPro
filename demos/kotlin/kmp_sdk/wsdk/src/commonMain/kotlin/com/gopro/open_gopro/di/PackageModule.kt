/* PackageModule.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.di

import com.gopro.open_gopro.OgpSdkAppContext
import com.gopro.open_gopro.connector.CameraConnector
import com.gopro.open_gopro.connector.GpBleConnector
import com.gopro.open_gopro.connector.GpDnsConnector
import com.gopro.open_gopro.connector.GpWifiConnector
import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import com.gopro.open_gopro.domain.network.IBleApi
import com.gopro.open_gopro.domain.network.IHttpApi
import com.gopro.open_gopro.gopro.GoProFactory
import com.gopro.open_gopro.network.KableBle
import com.gopro.open_gopro.network.KtorHttp
import kotlinx.coroutines.CoroutineDispatcher
import org.koin.dsl.module

internal fun buildPackageModules(dispatcher: CoroutineDispatcher, appContext: OgpSdkAppContext) =
    module {
      single<CoroutineDispatcher> { dispatcher }

      includes(buildOgpSdkPlatformModules(appContext))

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
      single<IGoProFactory> { GoProFactory(get(), get(), get(), get(), get()) }
    }
