package di

import WsdkAppContext
import org.koin.core.module.Module

expect fun buildPlatformModules(appContext: WsdkAppContext): Module
