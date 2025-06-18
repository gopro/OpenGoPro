/* AccessPointScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens.connected

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import presenter.AccessPointViewModel
import presenter.ApUiState
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.SnackbarMessageHandler

@Composable
fun AccessPointScreen(
    navController: NavController,
    viewModel: AccessPointViewModel,
    modifier: Modifier = Modifier,
) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  val errorMessage by viewModel.errorMessage.collectAsStateWithLifecycle()

  var ssid by remember { mutableStateOf("") }
  var password: String? by remember { mutableStateOf(null) }

  errorMessage?.let { SnackbarMessageHandler(it) }

  CommonTopBar(
      navController = navController,
      title = Screen.AccessPoint.route,
  ) { paddingValues ->
    DisposableEffect(viewModel) {
      viewModel.start()
      onDispose { viewModel.stop() }
    }
    Column(modifier.padding(paddingValues)) {
      Text("State: ${state.name}")
      when (val s = state) {
        ApUiState.Idle,
        ApUiState.Scanning,
        is ApUiState.Connected ->
            ScanScreen(
                isScanning = (s is ApUiState.Scanning),
                isConnected = (s is ApUiState.Connected),
                onScanStart = { viewModel.scanForSsids() },
                onSsidSelect = { ssid = it },
                selectedSsid = ssid,
                onDisconnect = { viewModel.disconnect() })

        is ApUiState.WaitingConnect -> {
          ScanScreen(
              isScanning = false,
              isConnected = false,
              onScanStart = { viewModel.scanForSsids() },
              onSsidSelect = { ssid = it },
              ssids = s.ssids,
              selectedSsid = ssid,
              onDisconnect = { viewModel.disconnect() })
          ConnectScreen(
              password = password,
              onConnectSsid = {
                password?.let { viewModel.connectToSsid(ssid, it) } ?: viewModel.connectToSsid(ssid)
              },
              onPasswordChange = { password = it })
        }

        is ApUiState.Connecting -> ConnectingScreen(s.ssid)
      }
    }
  }
}

@Composable
fun ScanScreen(
    isScanning: Boolean,
    isConnected: Boolean,
    ssids: List<String> = listOf(),
    onScanStart: (() -> Unit),
    onSsidSelect: ((String) -> Unit),
    selectedSsid: String,
    onDisconnect: (() -> Unit)
) {
  Column {
    Button(onScanStart) { Text("Start Scanning for SSIDS") }
    if (isConnected) {
      Button(onDisconnect) { Text("Disconnect") }
    }
    if (isScanning) {
      IndeterminateCircularProgressIndicator()
    }
    LazyColumn {
      items(ssids) { ssid ->
        val modifier = Modifier.clickable(onClick = { onSsidSelect(ssid) })
        if (ssid == selectedSsid) {
          modifier.border(BorderStroke(3.dp, Color.Green))
        }
        Row(modifier) {
          Column {
            Text(ssid)
            HorizontalDivider()
          }
        }
      }
    }
  }
}

@Composable
fun ConnectScreen(
    password: String?,
    onConnectSsid: () -> Unit,
    onPasswordChange: ((String) -> Unit)
) {
  TextField(
      value = password ?: "",
      onValueChange = { onPasswordChange(it) },
      label = { Text("Password") })
  Button(onConnectSsid) { Text("Connect") }
}

@Composable
fun ConnectingScreen(ssid: String) {
  Column {
    Text("Connecting to $ssid")
    IndeterminateCircularProgressIndicator()
  }
}
