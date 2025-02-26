/* WebcamScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens.connected

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
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
import com.gopro.open_gopro.operations.WebcamProtocol
import presenter.WebcamUiState
import presenter.WebcamViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.StreamPlayerWrapper

@Composable
fun WebcamScreen(
    navController: NavController,
    viewModel: WebcamViewModel,
    modifier: Modifier = Modifier,
) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  var protocol by remember { mutableStateOf(WebcamProtocol.TS) }

  CommonTopBar(
      navController = navController,
      title = Screen.Webcam.route,
  ) { paddingValues ->
    DisposableEffect(viewModel) {
      viewModel.start()
      onDispose { viewModel.stop() }
    }
    Column(modifier.padding(paddingValues)) {
      Text("State: ${state.message}")
      when (state) {
        WebcamUiState.Ready -> {
          Button({ viewModel.startStream(protocol) }) { Text("Start Stream") }
          //                    ProtocolSelectionDropDown { protocol = it }
        }

        is WebcamUiState.Starting -> IndeterminateCircularProgressIndicator()

        is WebcamUiState.Streaming -> {
          Button({ viewModel.stopStream() }) { Text("Stop Stream") }
          Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            StreamPlayerWrapper.player.PlayStream(modifier, viewModel.streamUrl(protocol))
          }
        }

        else -> {}
      }
    }
  }
}

@Composable
fun ProtocolSelectionDropDown(onProtocolSelect: ((WebcamProtocol) -> Unit)) {
  var expanded by remember { mutableStateOf(false) }
  Box(modifier = Modifier.fillMaxSize()) {
    Button({ expanded = true }) { Text("Select Streaming Protocol") }
    DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
      DropdownMenuItem(
          text = { Text("RTSP") },
          onClick = { onProtocolSelect(WebcamProtocol.RTSP) },
      )
      DropdownMenuItem(
          text = { Text("TS") },
          onClick = { onProtocolSelect(WebcamProtocol.TS) },
      )
    }
  }
}
