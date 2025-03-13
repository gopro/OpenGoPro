/* LivestreamScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens.connected

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import presenter.LivestreamUiState
import presenter.LivestreamViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.StreamPlayerWrapper

@Composable
fun LivestreamScreen(
    navController: NavController,
    viewModel: LivestreamViewModel,
    modifier: Modifier = Modifier,
) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  var url: String by remember { mutableStateOf("") }

  CommonTopBar(
      navController = navController,
      title = Screen.Livestream.route,
  ) { paddingValues ->
    DisposableEffect(viewModel) {
      viewModel.start()
      onDispose { viewModel.stop() }
    }
    Column(modifier.padding(paddingValues)) {
      Text("State: ${state.name}")
      when (state) {
        is LivestreamUiState.Ready -> {
          Button({ viewModel.startStream(url) }) { Text("Start Stream") }
          TextField(
              value = url, onValueChange = { url = it }, label = { Text("Livestream Server URL") })
        }

        is LivestreamUiState.Configuring -> IndeterminateCircularProgressIndicator()

        is LivestreamUiState.Streaming -> {
          Button({ viewModel.stopStream() }) { Text("Stop Stream") }
          Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            StreamPlayerWrapper.player.PlayStream(modifier, url)
          }
        }

        else -> {}
      }
    }
  }
}
