package di

import AppContext
import android.content.Context
import android.net.wifi.WifiManager
import connector.AndroidDnsApi
import connector.AndroidWifiApi
import data.AndroidDatabaseProvider
import database.IDatabaseProvider
import domain.network.IDnsApi
import domain.network.IHttpClientProvider
import domain.network.IWifiApi
import network.AndroidHttpClientProvider
import org.koin.dsl.bind
import org.koin.dsl.module

internal actual fun buildWsdkPlatformModule(appContext: AppContext): WsdkPlatformModule {
    return object : WsdkPlatformModule {
        val context = appContext.get()
        override val module = module {
            single<WifiManager> {
                context.getSystemService(Context.WIFI_SERVICE) as WifiManager
            }

            // This is instead of an expect / actual classes. It seemed a good pattern to conditionally pass context.
            // TODO can we make this an interface somehow? There is no compile-time enforcement of their existence.
            single { AndroidWifiApi(context, get(), get()) }.bind(IWifiApi::class)
            single { AndroidDnsApi(context, get()) }.bind(IDnsApi::class)
            single { AndroidDatabaseProvider(context) }.bind(IDatabaseProvider::class)
            single { AndroidHttpClientProvider }.bind(IHttpClientProvider::class)
        }
    }
}