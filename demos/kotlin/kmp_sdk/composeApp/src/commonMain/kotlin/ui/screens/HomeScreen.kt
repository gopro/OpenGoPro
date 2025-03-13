/* HomeScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.gopro.open_gopro.ScanResult
import presenter.CameraChooserUiState
import presenter.CameraChooserViewModel
import presenter.ScanNetworkType
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator

@Composable
fun HomeScreen(
    navController: NavController,
    viewModel: CameraChooserViewModel,
    modifier: Modifier = Modifier,
) {
  val devices by viewModel.devices.collectAsStateWithLifecycle()
  val state by viewModel.state.collectAsStateWithLifecycle()
  val selectedNetworks = remember { mutableStateListOf<ScanNetworkType>() }

  CommonTopBar(
      navController = navController,
      title = Screen.CameraChooser.route,
  ) { paddingValues ->
    if (state == CameraChooserUiState.Connected) {
      LaunchedEffect(state) { navController.navigate(Screen.Camera.route) }
    }
    Column(modifier.padding(paddingValues)) {
      Text("Current state: $state")
      NetworkTypeSelection(selectedNetworks) { network, check ->
        if (check) selectedNetworks.add(network) else selectedNetworks.remove(network)
      }
      DiscoverButton(
          state,
          onDiscover = { viewModel.discover(selectedNetworks.toSet()) },
          onCancel = viewModel::cancelDiscovery)
      HorizontalDivider()
      ScanResultList(devices) { viewModel.connect(it) }
      when (state) {
        is CameraChooserUiState.Discovering,
        is CameraChooserUiState.Connecting -> IndeterminateCircularProgressIndicator()
        else -> {}
      }
    }
  }
}

@Composable
fun DiscoverButton(state: CameraChooserUiState, onDiscover: (() -> Unit), onCancel: (() -> Unit)) {
  Column {
    Button({
      when (state) {
        CameraChooserUiState.Idle -> onDiscover()
        CameraChooserUiState.Discovering -> onCancel()
        else -> {} // TODO
      }
    }) {
      Text(state.name)
    }
  }
}

@Composable
fun ScanResultList(devices: List<ScanResult>, onDeviceSelect: (ScanResult) -> Unit) {
  LazyColumn {
    items(devices) { device ->
      Row(Modifier.clickable(onClick = { onDeviceSelect(device) })) {
        Column {
          Text(device.id.toString())
          Text(device.networkType.name)
          HorizontalDivider()
        }
      }
      HorizontalDivider()
    }
  }
}

@Composable
fun NetworkTypeSelection(
    networks: List<ScanNetworkType>,
    onCheck: (ScanNetworkType, Boolean) -> Unit
) {
  LazyColumn {
    items(ScanNetworkType.entries.toTypedArray()) { networkType ->
      Row {
        Checkbox(
            checked = networks.contains(networkType),
            onCheckedChange = { onCheck(networkType, it) })
        Text(networkType.name)
      }
    }
  }
}
