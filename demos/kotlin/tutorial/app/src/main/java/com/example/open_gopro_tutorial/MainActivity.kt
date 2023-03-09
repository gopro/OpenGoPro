/* MainActivity.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:15 UTC 2023 */

package com.example.open_gopro_tutorial

import android.app.Application
import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.Composable
import com.example.open_gopro_tutorial.network.Bluetooth
import com.example.open_gopro_tutorial.network.Wifi
import com.example.open_gopro_tutorial.ui.MainScreen
import com.example.open_gopro_tutorial.ui.MainViewModel
import com.example.open_gopro_tutorial.ui.theme.OpenGoProTutorialTheme

object DataStore {
    var connectedGoPro: String? = null
}

/**
 * AppContainer used by the rest of classes to obtain dependencies
 */
interface AppContainer {
    val applicationContext: Context
    val ble: Bluetooth
    val wifi: Wifi
}

class AppContainerImpl(override val applicationContext: Context) : AppContainer {
    override val ble = Bluetooth.getInstance(applicationContext)
    override val wifi = Wifi(applicationContext)
}

class TutorialApplication : Application() {
    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = AppContainerImpl(this)
    }
}

@Composable
fun TutorialApp(appContainer: AppContainer) {
    OpenGoProTutorialTheme {
        MainScreen(MainViewModel(appContainer))
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val appContainer = (application as TutorialApplication).container
        setContent { TutorialApp(appContainer) }
    }
}
