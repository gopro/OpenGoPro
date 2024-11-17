package di

import WsdkAppContext
import connector.AppleDnsApi
import connector.AppleWifiApi
import data.AppleDatabaseProvider
import database.IDatabaseProvider
import domain.network.IDnsApi
import domain.network.IHttpClientProvider
import domain.network.IWifiApi
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