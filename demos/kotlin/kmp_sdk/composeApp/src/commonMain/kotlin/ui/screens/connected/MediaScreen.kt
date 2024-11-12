package ui.screens.connected

import MediaMetadata
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
import entity.media.MediaId
import presenter.MediaUiState
import presenter.MediaViewModel
import ui.common.Screen
import ui.components.CommonTopBar
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
        title = Screen.Camera.route,
    ) { paddingValues ->
        Column(modifier.padding(paddingValues)) {
            DisposableEffect(viewModel) {
                // TODO is viewModel correct lifecycle owner?
                viewModel.start()
                onDispose { viewModel.stop() }
            }
            MediaListQueryButton { viewModel.getMediaList() }
            MediaGrid(mediaList) { viewModel.getMedia(it) }
            HorizontalDivider()
            when (val s = state) {
                is MediaUiState.Idle, MediaUiState.WaitingMediaSelection -> {}
                is MediaUiState.ActivePhoto -> {
                    MediaMetadata(s.photo, s.metadata)
                    PhotoDisplay.FromBinary(modifier, s.data)
                }

                is MediaUiState.ActiveVideo -> {
                    MediaMetadata(s.video, s.metadata)
                    // TODO put this back if / when we fix video display
//                    VideoPlayerWrapper.player.FromBinary(modifier, s.data)
                    PhotoDisplay.FromBinary(modifier, s.data)
                }
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
fun MediaListQueryButton(
    onGetMediaList: () -> Unit
) {
    Column {
        Button(onGetMediaList) { Text("Get Media List") }
    }
}

@Composable
fun MediaGrid(
    mediaList: List<MediaId>,
    onMediaSelect: (MediaId) -> Unit
) {
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
