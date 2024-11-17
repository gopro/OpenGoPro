package ui.components

import android.content.Context
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.util.EventLogger
import androidx.media3.ui.PlayerView

class `ExoplayerStreamPlayer.android.kt`(private val context: Context) : IStreamPlayer {
    @Composable
    override fun PlayStream(modifier: Modifier, url: String) {
        val exoPlayer = remember {
            ExoPlayer.Builder(context).build().apply {
                setMediaItem(MediaItem.fromUri(url))
                prepare()
            }
        }.apply {
            addAnalyticsListener(EventLogger())
        }

//        // Manage lifecycle events
//        DisposableEffect(Unit) {
//            onDispose {
//                exoPlayer.release()
//            }
//        }

        // Use AndroidView to embed an Android View (PlayerView) into Compose
        AndroidView(
            factory = {
                PlayerView(context).apply {
                    player = exoPlayer
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )
    }
}