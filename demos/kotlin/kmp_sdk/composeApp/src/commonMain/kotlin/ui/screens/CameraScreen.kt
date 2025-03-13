/* CameraScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import co.touchlab.kermit.Logger
import com.gopro.open_gopro.operations.CohnState
import presenter.CameraViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.MenuListItem
import ui.components.SnackbarMessageHandler

private val logger = Logger.withTag("CameraScreen")

@Composable
fun CameraScreen(
    navController: NavController,
    subRoutes: List<Screen>,
    viewModel: CameraViewModel,
    modifier: Modifier = Modifier,
) {
  val cohnState by viewModel.cohnState.collectAsStateWithLifecycle()
  val isBusy by viewModel.isBusy.collectAsStateWithLifecycle()
  val isBleConnected by viewModel.isBleConnected.collectAsStateWithLifecycle()
  val isHttpConnected by viewModel.isHttpConnected.collectAsStateWithLifecycle()
  val disconnect by viewModel.disconnects.collectAsStateWithLifecycle()

  disconnect?.let { SnackbarMessageHandler("$it disconnected!!") }

  CommonTopBar(
      navController = navController,
      title = Screen.Camera.route,
  ) { paddingValues ->
    Column(modifier.padding(paddingValues)) {
      DisposableEffect(viewModel) {
        viewModel.start()
        onDispose { viewModel.stop() }
      }

      if (isBleConnected) Text("BLE Connected")
      if (isHttpConnected) Text("HTTP Connected")
      isBusy?.let { busy ->
        IndeterminateCircularProgressIndicator()
        Text(busy.text)
      }
          ?: ReadyScreen(
              cohnState,
              subRoutes,
              viewModel::toggleShutter,
              { navController.navigate(it.route) },
              viewModel::connectWifi,
              viewModel::sleep)
    }
  }
}

@Composable
fun ReadyScreen(
    cohnState: CohnState,
    subRoutes: List<Screen>,
    onToggleShutter: () -> Unit,
    onSelectScreen: (Screen) -> Unit,
    onConnectWifi: (() -> Unit),
    onSleep: (() -> Unit)
) {
  //    Text("COHN state: $cohnState")
  Button(onToggleShutter) { Text("Toggle shutter") }
  Button(onConnectWifi) { Text("Connect Wi-Fi") }
  Button(onSleep) { Text("Sleep") }
  HorizontalDivider(thickness = 8.dp)

  LazyColumn {
    items(subRoutes) { screen ->
      MenuListItem(screen.route) {
        logger.d("Navigating to ${screen.route}")
        onSelectScreen(screen)
      }
    }
  }
}
