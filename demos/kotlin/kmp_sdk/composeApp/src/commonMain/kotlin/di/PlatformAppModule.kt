package di

import com.gopro.open_gopro.WsdkAppContext
import org.koin.core.module.Module

expect fun buildPlatformModules(appContext: WsdkAppContext): Module
