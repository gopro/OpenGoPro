/* VideoPlayer.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

interface IVideoPlayer {
  @Composable fun FromNetwork(modifier: Modifier, url: String)

  @Composable fun FromBinary(modifier: Modifier, data: ByteArray)
}

object VideoPlayerWrapper : KoinComponent {
  val player: IVideoPlayer by inject()
}
