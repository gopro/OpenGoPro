package di

import com.gopro.open_gopro.WsdkAppContext
import android.content.Context
import android.net.wifi.WifiManager
import com.gopro.open_gopro.di.WsdkPlatformModule
import connector.AndroidDnsApi
import connector.AndroidWifiApi
import data.AndroidDatabaseProvider
import com.gopro.open_gopro.database.IDatabaseProvider
import com.gopro.open_gopro.domain.network.IDnsApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.domain.network.IWifiApi
import network.AndroidHttpClientProvider
import org.koin.dsl.bind
import org.koin.dsl.module

internal actual fun buildWsdkPlatformModule(appContext: WsdkAppContext): WsdkPlatformModule {
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