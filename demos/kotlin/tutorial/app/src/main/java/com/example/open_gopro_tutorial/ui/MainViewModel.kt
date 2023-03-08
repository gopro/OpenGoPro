/* MainViewModel.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.ui

import android.util.Log
import androidx.annotation.RequiresPermission
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.open_gopro_tutorial.AppContainer
import com.example.open_gopro_tutorial.network.BleEventListener
import com.example.open_gopro_tutorial.network.WifiEventListener
import com.example.open_gopro_tutorial.tutorials.Tutorial
import com.example.open_gopro_tutorial.tutorials.Tutorials
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlinx.datetime.Clock
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime
import timber.log.Timber
import java.io.File

sealed interface MainUiState {
    val logEntries: List<String>
    val bleConnected: Boolean
    val wifiConnected: Boolean

    data class Idle(
        override val logEntries: List<String>,
        override val bleConnected: Boolean,
        override val wifiConnected: Boolean,
        val tutorials: List<Tutorial>
    ) : MainUiState

    data class TutorialSelected(
        override val logEntries: List<String>,
        override val bleConnected: Boolean,
        override val wifiConnected: Boolean,
        val activeTutorial: Tutorial,
        val inProgress: Boolean,
        val media: File?,
    ) : MainUiState

}

private data class MainViewModelState(
    val logEntries: SnapshotStateList<String> = mutableStateListOf(),
    val wifiConnected: Boolean = false,
    val tutorials: List<Tutorial> = Tutorials,
    val activeTutorial: Tutorial? = null,
    val goproBleAddress: String? = null,
    val tutorialInProgress: Boolean = false,
    val media: File? = null
) {
    val bleConnected get() = goproBleAddress != null

    fun toUiState(): MainUiState {
        return if (activeTutorial == null) {
            MainUiState.Idle(
                logEntries = logEntries,
                bleConnected = bleConnected,
                wifiConnected = wifiConnected,
                tutorials = tutorials.filterNot { tutorial ->
                    (tutorial.requiresBle and !bleConnected) || (tutorial.requiresWifi and !wifiConnected)
                })
        } else {
            MainUiState.TutorialSelected(
                logEntries = logEntries,
                bleConnected = goproBleAddress != null,
                wifiConnected = wifiConnected,
                activeTutorial = activeTutorial,
                inProgress = tutorialInProgress,
                media = media
            )
        }
    }
}

class MainViewModel(private val appContainer: AppContainer) : ViewModel() {
    private val viewModelState: MutableStateFlow<MainViewModelState> =
        MutableStateFlow(MainViewModelState())
    val uiState: StateFlow<MainUiState> = viewModelState.map(MainViewModelState::toUiState).stateIn(
        viewModelScope, SharingStarted.Eagerly, viewModelState.value.toUiState()
    )

    // Internal flow to ensure in-order logs
    private val logs = MutableSharedFlow<String>()

    private val timberTree = object : Timber.DebugTree() {
        override fun log(
            priority: Int, tag: String?, message: String, t: Throwable?
        ) {
            // Append GoPro tag for easy logcat filtering
            super.log(priority, "GP_$tag", message, t)

            // Send these logs to UI
            if (priority >= Log.DEBUG) viewModelScope.launch { logs.emit(message) }
        }
    }

    private val bleListeners by lazy {
        BleEventListener().apply {
            onConnect =
                { device -> viewModelState.update { it.copy(goproBleAddress = device.address) } }
            onDisconnect = { device ->
                if (device.address == viewModelState.value.goproBleAddress) {
                    viewModelState.update { it.copy(goproBleAddress = null) }
                }
            }
        }
    }

    private val wifiListeners by lazy {
        // We assume the only network change will be for the OGP tutorials
        WifiEventListener().apply {
            onConnect = { viewModelState.update { it.copy(wifiConnected = true) } }
            onDisconnect = { viewModelState.update { it.copy(wifiConnected = false) } }
        }
    }

    init {
        Timber.plant(timberTree)
        // Register for network connection change updates for all connections
        appContainer.ble.registerListener(bleListeners)
        appContainer.wifi.registerListener(wifiListeners)

        // Continuously check for log messages
        viewModelScope.launch { logs.collect { updateLog(it) } }
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    fun onTutorialSelect(tutorial: Tutorial?) {
        tutorial?.let {
            appContainer.ble.enableAdapter()
            appContainer.wifi.enableAdapter()
        }
        viewModelState.update { it.copy(activeTutorial = tutorial, tutorialInProgress = true) }
        tutorial?.let {
            viewModelScope.launch {
                val file = it.perform(appContainer)
                viewModelState.update { it.copy(tutorialInProgress = false, media = file) }
            }.invokeOnCompletion { cause ->
                Timber.e(cause)
                viewModelState.update { it.copy(tutorialInProgress = false) }
            }
        } ?: run {
            // Null tutorial means go back to the selection screen
            viewModelState.update { it.copy(logEntries = mutableStateListOf()) }
        }
    }

    fun updateLog(message: String) {
        val time = Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault())
        val hour = "%02d".format(time.hour)
        val minutes = "%02d".format(time.minute)
        val seconds = "%02d".format(time.second)
        val ms = "%03.0f".format(time.nanosecond.toDouble() / 1000000)

        viewModelState.update {
            it.copy(logEntries = viewModelState.value.logEntries.also { entries ->
                entries.add("$hour:$minutes:$seconds.$ms ::: $message")
            })
        }
    }
}