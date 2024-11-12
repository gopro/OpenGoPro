package di

import org.koin.core.module.Module
import org.koin.dsl.module

interface PlatformModule {
    val module: Module
}

expect val platformModule: PlatformModule

fun buildPlatformModules() = module {
    includes(platformModule.module)
}