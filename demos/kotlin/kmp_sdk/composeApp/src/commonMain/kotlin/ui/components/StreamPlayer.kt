/* StreamPlayer.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

interface IStreamPlayer {
  @Composable fun PlayStream(modifier: Modifier, url: String)
}

object StreamPlayerWrapper : KoinComponent {
  val player: IStreamPlayer by inject()
}
