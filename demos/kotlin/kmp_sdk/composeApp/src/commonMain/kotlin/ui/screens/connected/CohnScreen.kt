package ui.screens.connected

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import presenter.CohnUiState
import presenter.CohnViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator

@Composable
fun CohnScreen(
    navController: NavController,
    viewModel: CohnViewModel,
    modifier: Modifier = Modifier,
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    CommonTopBar(
        navController = navController,
        title = Screen.Cohn.route,
    ) { paddingValues ->
        DisposableEffect(viewModel) {
            viewModel.start()
            onDispose { viewModel.stop() }
        }
        Column(modifier.padding(paddingValues)) {
            Text("COHN state: ${state.name}")
            Button({ viewModel.enable() }) { Text("Enable") }
            Button({ viewModel.disable() }) { Text("Disable") }
            Button({ viewModel.provision() }) { Text("Provision") }
            Button({ viewModel.unprovision() }) { Text("Unprovision") }
            if (state == CohnUiState.Provisioning) {
                IndeterminateCircularProgressIndicator()
            }
        }
    }
}
