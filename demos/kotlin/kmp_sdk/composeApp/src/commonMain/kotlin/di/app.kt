package di

import com.gopro.open_gopro.WsdkAppContext
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildAppModule(appContext: WsdkAppContext): Module =
    module {
        includes(dataModule)
        includes(buildPlatformModules(appContext))
        includes(screenModules)
        includes(buildWsdkModule(appContext))
    }