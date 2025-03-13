/* MainViewController.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package gopro.open_gopro

import App
import androidx.compose.ui.window.ComposeUIViewController
import com.gopro.open_gopro.OgpSdkAppContext
import di.buildAppModule
import org.koin.core.context.startKoin
import org.koin.core.logger.Level
import org.koin.core.logger.PrintLogger
import platform.UIKit.UIViewController

fun MainViewController(): UIViewController {
  startKoin {
    PrintLogger(Level.WARNING)
    modules(buildAppModule(appContext = OgpSdkAppContext()))
  }
  return ComposeUIViewController { App() }
}
