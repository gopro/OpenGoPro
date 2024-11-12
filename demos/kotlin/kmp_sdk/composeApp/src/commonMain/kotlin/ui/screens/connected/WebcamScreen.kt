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
import entity.operation.WebcamProtocol
import presenter.WebcamViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.StreamPlayerWrapper

@Composable
fun WebcamScreen(
    navController: NavController,
    viewModel: WebcamViewModel,
    modifier: Modifier = Modifier,
) {
    val status by viewModel.status.collectAsStateWithLifecycle()
    val error by viewModel.error.collectAsStateWithLifecycle()
    var protocol by remember { mutableStateOf(WebcamProtocol.RTSP) }

    CommonTopBar(
        navController = navController,
        title = Screen.Webcam.route,
    ) { paddingValues ->
        DisposableEffect(viewModel) {
            // TODO is viewModel correct lifecycle owner?
            viewModel.start()
            onDispose { viewModel.stop() }
        }
        Column(modifier.padding(paddingValues)) {
            Text("Wireless Webcam Stream")
            Text("Status: ${status.name}")
            Text("Error: ${error.name}")
            Button({ viewModel.startStream(protocol) }) { Text("Start Stream") }
            Button({ viewModel.stopStream() }) { Text("Stop Stream") }
            if (status.isStreaming()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    StreamPlayerWrapper.player.PlayStream(modifier, viewModel.streamUrl)
                }
            }
            ProtocolSelectionDropDown { protocol = it }
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