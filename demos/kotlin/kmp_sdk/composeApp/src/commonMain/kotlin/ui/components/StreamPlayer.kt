package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

interface IStreamPlayer {
    @Composable
    fun PlayStream(modifier: Modifier, url: String)
}

object StreamPlayerWrapper: KoinComponent {
    val player: IStreamPlayer by inject()
}