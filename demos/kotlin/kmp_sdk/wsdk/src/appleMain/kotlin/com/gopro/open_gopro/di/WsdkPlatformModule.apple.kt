/* WsdkPlatformModule.apple.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.di

import com.gopro.open_gopro.OgpSdkAppContext
import com.gopro.open_gopro.connector.AppleDnsApi
import com.gopro.open_gopro.connector.AppleWifiApi
import com.gopro.open_gopro.data.AppleDatabaseProvider
import com.gopro.open_gopro.database.IDatabaseProvider
import com.gopro.open_gopro.domain.network.IDnsApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.domain.network.IWifiApi
import com.gopro.open_gopro.network.AppleHttpClientProvider
import org.koin.dsl.bind
import org.koin.dsl.module

internal actual fun buildOgpSdkPlatformModule(appContext: OgpSdkAppContext): OgpSdkPlatformModule {
  return object : OgpSdkPlatformModule {
    override val module = module {
      single { AppleWifiApi(get()) }.bind(IWifiApi::class)
      single { AppleDnsApi(get()) }.bind(IDnsApi::class)
      single { AppleDatabaseProvider() }.bind(IDatabaseProvider::class)
      single { AppleHttpClientProvider() }.bind(IHttpClientProvider::class)
    }
  }
}
