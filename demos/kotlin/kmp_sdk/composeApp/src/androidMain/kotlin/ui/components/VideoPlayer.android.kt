/* VideoPlayer.android.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package ui.components

import android.content.Context
import android.net.Uri
import androidx.annotation.OptIn
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.util.UnstableApi
import androidx.media3.datasource.ByteArrayDataSource
import androidx.media3.datasource.DataSource
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.source.ProgressiveMediaSource
import androidx.media3.ui.PlayerView

// https://medium.com/@adman.shadman/creating-a-cross-platform-video-player-component-in-kotlin-multiplatform-android-ios-9d79174aa2ca

class AndroidVideoPlayer(private val context: Context) : IVideoPlayer {
  //    @Composable
  //    override fun FromNetwork(modifier: Modifier, url: String) {
  //        AndroidView(
  //            modifier = modifier.fillMaxSize(),
  //            factory = { context ->
  //                VideoView(context).apply {
  //                    setVideoPath(url)
  //                    val mediaController = MediaController(context)
  //                    mediaController.setAnchorView(this)
  //                    setMediaController(mediaController)
  //                    setOnPreparedListener { start() }
  //                    setOnErrorListener { _, _, _ -> true }
  //                    layoutParams = FrameLayout.LayoutParams(
  //                        FrameLayout.LayoutParams.MATCH_PARENT,
  //                        FrameLayout.LayoutParams.MATCH_PARENT
  //                    )
  //                }
  //            },
  //            update = { it.start() }
  //        )
  //    }

  @Composable
  override fun FromNetwork(modifier: Modifier, url: String) {
    val exoPlayer = remember {
      ExoPlayer.Builder(context).build().apply {
        setMediaItem(MediaItem.fromUri(url))
        prepare()
      }
    }

    // Use AndroidView to embed an Android View (PlayerView) into Compose
    AndroidView(
        factory = { PlayerView(context).apply { player = exoPlayer } },
        modifier = Modifier.fillMaxWidth().height(200.dp))
  }

  @OptIn(UnstableApi::class)
  @Composable
  override fun FromBinary(modifier: Modifier, data: ByteArray) {
    val dataSource = ByteArrayDataSource(data)
    val dataSourceFactory = DataSource.Factory { dataSource }
    val mediaSourceFactory = ProgressiveMediaSource.Factory(dataSourceFactory)
    val mediaSource = mediaSourceFactory.createMediaSource(MediaItem.fromUri(Uri.EMPTY))
    val exoPlayer = remember {
      ExoPlayer.Builder(context).build().apply {
        addMediaSource(mediaSource)
        prepare()
      }
    }

    AndroidView(
        factory = { PlayerView(context).apply { player = exoPlayer } },
        modifier = Modifier.fillMaxWidth().height(200.dp))
  }
}
