package ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import co.touchlab.kermit.Logger
import domain.gopro.CohnState
import entity.queries.Resolution
import presenter.CameraUiState
import presenter.CameraViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.MenuListItem

@Composable
fun CameraScreen(
    navController: NavController,
    subRoutes: List<Screen>,
    viewModel: CameraViewModel,
    modifier: Modifier = Modifier,
) {
    val uiState by viewModel.state.collectAsStateWithLifecycle()
    val resolution by viewModel.resolution.collectAsStateWithLifecycle()
    val cohnState by viewModel.cohnState.collectAsStateWithLifecycle()

    CommonTopBar(
        navController = navController,
        title = Screen.Camera.route,
    ) { paddingValues ->
        Column(modifier.padding(paddingValues)) {
            when (uiState) {
                is CameraUiState.Idle ->
                    // https://developer.android.com/develop/ui/compose/side-effects
                    DisposableEffect(viewModel) {
                        // TODO is viewModel correct lifecycle owner?
                        viewModel.start()
                        onDispose { viewModel.stop() }
                    }

                is CameraUiState.Initializing -> ConnectingScreen()
                is CameraUiState.Ready ->
                    ReadyScreen(
                        resolution,
                        cohnState,
                        subRoutes,
                        viewModel::toggleShutter,
                        viewModel::registerResolutionValueUpdates,
                        { navController.navigate(it.route) },
                        viewModel::connectWifi
                    )
            }
        }
    }
}

@Composable
fun ConnectingScreen() {
    Text("Connecting BLE...")
    IndeterminateCircularProgressIndicator()
}

@Composable
fun ReadyScreen(
    resolution: Resolution,
    cohnState: CohnState,
    subRoutes: List<Screen>,
    onToggleShutter: () -> Unit,
    onRegisterResolutionValueUpdates: () -> Unit,
    onSelectScreen: (Screen) -> Unit,
    onConnectWifi: (() -> Unit)
) {
    // TODO remove this. Just for initial testing.
    Text("Current Resolution: $resolution")
    Text("COHN state: $cohnState")
    Button(onToggleShutter) { Text("Toggle shutter") }
    Button(onRegisterResolutionValueUpdates) { Text("Register for Resolution Value Updates") }
    Button(onConnectWifi) { Text("Connect Wi-Fi") }

    LazyColumn {
        items(subRoutes) { screen ->
            MenuListItem(screen.route) {
                Logger.d("Navigate to ${screen.route}")
                onSelectScreen(screen)
            }
        }
    }
}