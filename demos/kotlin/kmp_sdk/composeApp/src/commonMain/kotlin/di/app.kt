package di

import AppContext
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildAppModule(appContext: AppContext): Module =
    module {
        includes(dataModule)
        includes(buildPlatformModules(appContext))
        includes(screenModules)
        includes(buildWsdkModule(appContext))
    }