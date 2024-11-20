package gopro.open_gopro

import App
import WsdkAppContext
import androidx.compose.ui.window.ComposeUIViewController
import di.buildAppModule
import org.koin.core.context.startKoin
import org.koin.core.logger.Level
import org.koin.core.logger.PrintLogger
import platform.UIKit.UIViewController

fun MainViewController(): UIViewController {
    startKoin {
        PrintLogger(Level.WARNING)
        modules(buildAppModule(appContext = WsdkAppContext()))
    }
    return ComposeUIViewController { App() }
}