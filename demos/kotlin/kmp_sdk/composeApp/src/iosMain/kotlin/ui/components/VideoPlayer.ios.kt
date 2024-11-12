package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

@Composable
actual fun VideoPlayer(
    modifier: Modifier,
    url: String,
    isLandscape: Boolean,
    shouldStop: Boolean,
    onMediaReadyToPlay: () -> Unit
) {
}