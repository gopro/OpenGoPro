package ui.screens.connected

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
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
    val state by viewModel.state.collectAsStateWithLifecycle()

    val resolution by viewModel.resolution.collectAsStateWithLifecycle()

    CommonTopBar(
        navController = navController,
        title = Screen.AccessPoint.route,
    ) { paddingValues ->
        DisposableEffect(viewModel) {
            viewModel.start()
            onDispose { viewModel.stop() }
        }
        Column(modifier.padding(paddingValues)) {
            Text("Settings Screen")
        }
    }
}