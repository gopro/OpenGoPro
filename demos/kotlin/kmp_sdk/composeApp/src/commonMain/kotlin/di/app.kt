package di

import org.koin.dsl.KoinAppDeclaration
import org.koin.dsl.module

fun buildAppModule(config: KoinAppDeclaration? = null) =
    module {
        includes(dataModule)
        includes(buildPlatformModules())
        includes(screenModules)
//        includes(uiModules)
        includes(buildWsdkModule(config))
    }