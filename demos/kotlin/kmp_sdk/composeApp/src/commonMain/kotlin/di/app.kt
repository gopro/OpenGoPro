/* app.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package di

import com.gopro.open_gopro.OgpSdkAppContext
import org.koin.core.module.Module
import org.koin.dsl.module

fun buildAppModule(appContext: OgpSdkAppContext): Module = module {
  includes(dataModule)
  includes(buildPlatformModules(appContext))
  includes(screenModules)
  includes(buildOgpSdkModule(appContext))
}
