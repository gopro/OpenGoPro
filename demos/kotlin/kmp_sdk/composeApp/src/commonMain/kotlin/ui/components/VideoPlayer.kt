package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

interface IVideoPlayer {
    @Composable
    fun FromNetwork(modifier: Modifier, url: String)

    @Composable
    fun FromBinary(modifier: Modifier, data: ByteArray)
}

object VideoPlayerWrapper: KoinComponent {
    val player: IVideoPlayer by inject()
}