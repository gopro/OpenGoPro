package di

import com.gopro.open_gopro.OgpSdkAppContext
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildAppModule(appContext: OgpSdkAppContext): Module =
    module {
        includes(dataModule)
        includes(buildPlatformModules(appContext))
        includes(screenModules)
        includes(buildOgpSdkModule(appContext))
    }