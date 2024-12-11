package di

import com.gopro.open_gopro.WsdkAppContext
import com.gopro.open_gopro.di.WsdkPlatformModule
import connector.AppleDnsApi
import connector.AppleWifiApi
import data.AppleDatabaseProvider
import com.gopro.open_gopro.database.IDatabaseProvider
import com.gopro.open_gopro.domain.network.IDnsApi
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.domain.network.IWifiApi
import network.AppleHttpClientProvider
import org.koin.dsl.bind
import org.koin.dsl.module

internal actual fun buildWsdkPlatformModule(appContext: WsdkAppContext): WsdkPlatformModule {
    return object : WsdkPlatformModule { override val module = module {
            single { AppleWifiApi(get()) }.bind(IWifiApi::class)
            single { AppleDnsApi(get()) }.bind(IDnsApi::class)
            single { AppleDatabaseProvider() }.bind(IDatabaseProvider::class)
            single { AppleHttpClientProvider() }.bind(IHttpClientProvider::class)
        }
    }
}