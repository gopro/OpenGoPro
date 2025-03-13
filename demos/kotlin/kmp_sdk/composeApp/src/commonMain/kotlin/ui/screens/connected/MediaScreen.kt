/* MediaScreen.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:27 UTC 2025 */

package ui.screens.connected

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.gopro.open_gopro.operations.MediaId
import com.gopro.open_gopro.operations.MediaMetadata
import presenter.MediaUiState
import presenter.MediaViewModel
import ui.common.Screen
import ui.components.CommonTopBar
import ui.components.IndeterminateCircularProgressIndicator
import ui.components.PhotoDisplay

@Composable
fun MediaScreen(
    navController: NavController,
    viewModel: MediaViewModel,
    modifier: Modifier = Modifier,
) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  val mediaList by viewModel.mediaList.collectAsStateWithLifecycle()

  CommonTopBar(
      navController = navController,
      title = Screen.Media.route,
  ) { paddingValues ->
    Column(modifier.padding(paddingValues)) {
      DisposableEffect(viewModel) {
        viewModel.start()
        onDispose { viewModel.stop() }
      }
      Text("State: ${state.message}")

      // Always display user controls if not in error state
      if (state !is MediaUiState.Error) {
        MediaListQueryButton { viewModel.getMediaList() }
        MediaGrid(mediaList) { viewModel.getMedia(it) }
        HorizontalDivider()
      }
      // Display progress indicator if accessing media
      if (state is MediaUiState.RetrievingMedia) {
        IndeterminateCircularProgressIndicator()
      }

      // Display video / photo
      when (val s = state) {
        is MediaUiState.ActivePhoto -> {
          MediaMetadata(s.photo, s.metadata)
          PhotoDisplay.FromBinary(modifier, s.data)
        }

        is MediaUiState.ActiveVideo -> {
          MediaMetadata(s.video, s.metadata)
          // TODO download and store videos to disk.
          //                    VideoPlayerWrapper.player.FromBinary(modifier, s.data)
          PhotoDisplay.FromBinary(modifier, s.data)
        }
        else -> {}
      }
    }
  }
}

@Composable
fun MediaMetadata(item: MediaId, metadata: MediaMetadata) {
  Text("Chosen Media: ${item.asPath}")
  with(metadata) {
    Text("id: $id")
    Text("file size: $fileSize")
    Text("context type:  ${contentType.name}")
    Text("height: $height")
    Text("width: $width")
  }
}

@Composable
fun MediaListQueryButton(onGetMediaList: () -> Unit) {
  Column { Button(onGetMediaList) { Text("Get Media List") } }
}

@Composable
fun MediaGrid(mediaList: List<MediaId>, onMediaSelect: (MediaId) -> Unit) {
  LazyColumn {
    items(mediaList.take(5)) { mediaId ->
      Row(Modifier.clickable(onClick = { onMediaSelect(mediaId) })) {
        Column {
          Text(mediaId.asPath)
          HorizontalDivider()
        }
      }
    }
  }
}
