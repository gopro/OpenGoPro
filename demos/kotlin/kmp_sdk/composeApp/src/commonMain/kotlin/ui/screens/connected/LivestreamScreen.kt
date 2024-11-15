package ui.screens.connected

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import presenter.LivestreamUiState
import presenter.LivestreamViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.StreamPlayerWrapper

@Composable
fun LivestreamScreen(
    navController: NavController,
    viewModel: LivestreamViewModel,
    modifier: Modifier = Modifier,
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

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
            if (state is LivestreamUiState.Ready)
                Button({ viewModel.startStream() }) { Text("Start Stream") }
            if (state is LivestreamUiState.Streaming) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    StreamPlayerWrapper.player.PlayStream(modifier, viewModel.hlsUrl)
                }
            }
        }
    }
}