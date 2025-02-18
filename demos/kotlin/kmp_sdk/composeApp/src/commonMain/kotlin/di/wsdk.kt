package di

import com.gopro.open_gopro.OgpSdk
import com.gopro.open_gopro.OgpSdkAppContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildOgpSdkModule(appContext: OgpSdkAppContext): Module {
    return module {
        single<OgpSdk> { OgpSdk(Dispatchers.IO, appContext) }
    }
}