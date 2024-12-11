package di

import com.gopro.open_gopro.Wsdk
import com.gopro.open_gopro.WsdkAppContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildWsdkModule(appContext: WsdkAppContext): Module {
    return module {
        single<Wsdk> { Wsdk(Dispatchers.IO, appContext) }
    }
}