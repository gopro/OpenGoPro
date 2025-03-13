/* LibVlcStreamPlayer.android.kt.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package ui.components

import android.content.Context
import android.net.Uri
import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import co.touchlab.kermit.Logger
import org.videolan.BuildConfig
import org.videolan.libvlc.LibVLC
import org.videolan.libvlc.Media
import org.videolan.libvlc.MediaPlayer
import org.videolan.libvlc.util.VLCVideoLayout

private val logger = Logger.withTag("LibVlcStreamPlayer")

// https://stackoverflow.com/questions/76938888/handling-buffering-or-error-events-in-libvlc-when-video-data-is-incomplete
// https://tehleelmir.medium.com/how-to-integrate-vlc-or-vlclib-in-android-kotlin-798686844394

class LibVlcStreamPlayer(private val context: Context) : IStreamPlayer {
  private fun MediaPlayer.playMediaSource(vlcLib: LibVLC, source: Uri) {
    stop()
    Media(vlcLib, source)
        .apply {
          setHWDecoderEnabled(true, false)
          media = this
        }
        .release()
    play()
  }

  @Composable
  override fun PlayStream(modifier: Modifier, url: String) {
    logger.i("Playing stream from $url")

    val libVlc = remember {
      LibVLC(
          context,
          ArrayList<String>().apply {
            //            add("--no-drop-late-frames")
            //            add("--no-skip-frames")
            //            add("--file-caching=1500")

            add("--network-caching=150")
            add("--clock-jitter=0")
            add("--live-caching=150")
            add("--drop-late-frames")
            add("--skip-frames")
            add("--vout=android-display")
            add("--sout-transcode-vb=20")
            add("--no-audio")
            add(
                "--sout=#transcode{vcodec=h264,vb=20,acodec=mpga,ab=128,channels=2,samplerate=44100}:duplicate{dst=display}")
            add("--sout-x264-nf")
            if (BuildConfig.DEBUG) {
              add("-vvv")
            }
          })
    }

    val vlcView = remember {
      VLCVideoLayout(context).apply {
        keepScreenOn = true
        fitsSystemWindows = false
        layoutParams =
            FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
      }
    }

    val player = remember { MediaPlayer(libVlc).apply { attachViews(vlcView, null, true, false) } }

    AndroidView(modifier = modifier.fillMaxWidth(), factory = { vlcView })

    LaunchedEffect(Unit) {
      player.setEventListener { event ->
        // TODO handle these?
      }
      player.playMediaSource(libVlc, Uri.parse(url))
    }

    DisposableEffect(Unit) {
      onDispose {
        logger.d("Disposing of stream viewer.")
        player.release()
        libVlc.release()
      }
    }
  }
}
