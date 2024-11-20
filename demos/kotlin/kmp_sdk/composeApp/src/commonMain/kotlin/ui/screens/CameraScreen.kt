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
import entity.operation.CohnState
import entity.queries.Resolution
import presenter.CameraViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.MenuListItem

private val logger = Logger.withTag("CameraScreen")

@Composable
fun CameraScreen(
    navController: NavController,
    subRoutes: List<Screen>,
    viewModel: CameraViewModel,
    modifier: Modifier = Modifier,
) {
    val resolution by viewModel.resolution.collectAsStateWithLifecycle()
    val cohnState by viewModel.cohnState.collectAsStateWithLifecycle()
    val isBusy by viewModel.isBusy.collectAsStateWithLifecycle()
    val isBleConnected by viewModel.isBleConnected.collectAsStateWithLifecycle()
    val isHttpConnected by viewModel.isHttpConnected.collectAsStateWithLifecycle()

    CommonTopBar(
        navController = navController,
        title = Screen.Camera.route,
    ) { paddingValues ->
        Column(modifier.padding(paddingValues)) {
            // https://developer.android.com/develop/ui/compose/side-effects
            DisposableEffect(viewModel) {
                viewModel.start()
                onDispose { viewModel.stop() }
            }
            if (isBleConnected) Text("BLE Connected")
            if (isHttpConnected) Text("HTTP Connected")
            isBusy?.let { busy ->
                IndeterminateCircularProgressIndicator()
                Text(busy.text)
            } ?: ReadyScreen(
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

// TODO show connections

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
    Text("Current Resolution: $resolution")
//    Text("COHN state: $cohnState")
    Button(onToggleShutter) { Text("Toggle shutter") }
    Button(onRegisterResolutionValueUpdates) { Text("Register for Resolution Value Updates") }
    Button(onConnectWifi) { Text("Connect Wi-Fi") }

    LazyColumn {
        items(subRoutes) { screen ->
            MenuListItem(screen.route) {
                logger.d("Navigating to ${screen.route}")
                onSelectScreen(screen)
            }
        }
    }
}