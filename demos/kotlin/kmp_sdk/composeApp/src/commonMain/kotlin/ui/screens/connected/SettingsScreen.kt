/* SettingsScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens.connected

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Done
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import presenter.SettingsViewModel
import ui.common.Screen
import ui.components.CommonTopBar

@Composable
fun SettingsScreen(
    navController: NavController,
    viewModel: SettingsViewModel,
    modifier: Modifier = Modifier,
) {
  val currentResolution by viewModel.currentResolution.collectAsStateWithLifecycle()
  val resolutionCaps by viewModel.resolutionCaps.collectAsStateWithLifecycle()
  val currentFps by viewModel.currentFps.collectAsStateWithLifecycle()
  val fpsCaps by viewModel.fpsCaps.collectAsStateWithLifecycle()
  val currentFov by viewModel.currentFov.collectAsStateWithLifecycle()
  val fovCaps by viewModel.fovCaps.collectAsStateWithLifecycle()
  val battery by viewModel.currentBattery.collectAsStateWithLifecycle()
  val isBusy by viewModel.isBusy.collectAsStateWithLifecycle()
  val isEncoding by viewModel.isEncoding.collectAsStateWithLifecycle()

  CommonTopBar(
      navController = navController,
      title = Screen.Settings.route,
  ) { paddingValues ->
    DisposableEffect(viewModel) {
      viewModel.start()
      onDispose { viewModel.stop() }
    }
    Column(modifier.padding(paddingValues)) {
      Text("Settings")
      Text("Resolution: $currentResolution")
      SettingChipRow(resolutionCaps, currentResolution) { viewModel.setResolution(it) }
      Text("FPS: $currentFps")
      SettingChipRow(fpsCaps, currentFps) { viewModel.setFps(it) }
      Text("FOV: $currentFov")
      SettingChipRow(fovCaps, currentFov) { viewModel.setFov(it) }
      HorizontalDivider(thickness = 10.dp)
      Text("Statuses")
      Text("Battery: $battery")
      Text("isBusy: $isBusy")
      Text("isEncoding: $isEncoding")
    }
  }
}

@Composable
fun <T> SettingChipRow(capabilities: List<T>, current: T, onSelectSetting: ((T) -> Unit)) {
  LazyRow {
    items(capabilities) { setting ->
      SettingChip(setting.toString(), setting == current) { onSelectSetting(setting) }
    }
  }
}

@Composable
fun SettingChip(text: String, isHighlighted: Boolean, onSelect: (() -> Unit)) {
  FilterChip(
      onClick = onSelect,
      label = { Text(text) },
      selected = isHighlighted,
      leadingIcon =
          if (isHighlighted) {
            {
              Icon(
                  imageVector = Icons.Filled.Done,
                  contentDescription = "Done icon",
                  modifier = Modifier.size(FilterChipDefaults.IconSize))
            }
          } else {
            null
          },
  )
}
