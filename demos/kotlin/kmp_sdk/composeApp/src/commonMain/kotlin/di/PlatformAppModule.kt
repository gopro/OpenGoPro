package di

import AppContext
import org.koin.core.module.Module

expect fun buildPlatformModules(appContext: AppContext): Module
