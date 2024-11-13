package di

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
import org.koin.android.ext.koin.androidContext
import org.koin.dsl.bind
import org.koin.dsl.module

actual val wsdkPlatformModule = object : WsdkPlatformModule {
    override val module = module {
        single<WifiManager> {
            androidContext().getSystemService(Context.WIFI_SERVICE) as WifiManager
        }

        // This is instead of an expect / actual classes. It seemed a good pattern to conditionally pass context.
        // TODO can we make this an interface somehow? There is no compile-time enforcement of their existence.
        single { AndroidWifiApi(androidContext(), get(), get()) }.bind(IWifiApi::class)
        single { AndroidDnsApi(androidContext(), get()) }.bind(domain.network.IDnsApi::class)
        single { AndroidDatabaseProvider(androidContext()) }.bind(IDatabaseProvider::class)
        single { AndroidHttpClientProvider }.bind(IHttpClientProvider::class)
    }
}