package di

import com.gopro.open_gopro.OgpSdkAppContext
import org.koin.core.module.Module

expect fun buildPlatformModules(appContext: OgpSdkAppContext): Module
