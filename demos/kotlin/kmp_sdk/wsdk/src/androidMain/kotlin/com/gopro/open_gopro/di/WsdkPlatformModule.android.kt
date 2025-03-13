/* WsdkPlatformModule.android.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.di

import android.content.Context
import android.net.wifi.WifiManager
import com.gopro.open_gopro.OgpSdkAppContext
import com.gopro.open_gopro.connector.AndroidDnsApi
import com.gopro.open_gopro.connector.AndroidWifiApi
import com.gopro.open_gopro.data.AndroidDatabaseProvider
import com.gopro.open_gopro.database.IDatabaseProvider
import com.gopro.open_gopro.domain.network.IDnsApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.domain.network.IWifiApi
import com.gopro.open_gopro.network.AndroidHttpClientProvider
import org.koin.dsl.bind
import org.koin.dsl.module

internal actual fun buildOgpSdkPlatformModule(appContext: OgpSdkAppContext): OgpSdkPlatformModule {
  return object : OgpSdkPlatformModule {
    val context = appContext.get()
    override val module = module {
      single<WifiManager> { context.getSystemService(Context.WIFI_SERVICE) as WifiManager }

      // This is instead of an expect / actual classes. It seemed a good pattern to conditionally
      // pass context.
      // TODO can we make this an interface somehow? There is no compile-time enforcement of their
      // existence.
      single { AndroidWifiApi(context, get(), get()) }.bind(IWifiApi::class)
      single { AndroidDnsApi(context, get()) }.bind(IDnsApi::class)
      single { AndroidDatabaseProvider(context) }.bind(IDatabaseProvider::class)
      single { AndroidHttpClientProvider }.bind(IHttpClientProvider::class)
    }
  }
}
