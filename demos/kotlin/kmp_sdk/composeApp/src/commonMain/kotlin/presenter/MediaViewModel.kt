package presenter

import com.gopro.open_gopro.Wsdk
import androidx.lifecycle.viewModelScope
import data.IAppPreferences
import com.gopro.open_gopro.operations.MediaId
import com.gopro.open_gopro.operations.MediaMetadata
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class MediaUiState(val message: String) {
    data class Error(val error: String): MediaUiState("Error: $error")
    data object Ready : MediaUiState("Waiting for user interaction")
    data class RetrievingMedia(val media: MediaId): MediaUiState("Retrieving ${media.asPath}")
    data class ActivePhoto(val photo: MediaId, val metadata: MediaMetadata, val data: ByteArray) :
        MediaUiState("selected photo: ${photo.asPath}")

    data class ActiveVideo(val video: MediaId, val metadata: MediaMetadata, val data: ByteArray) :
        MediaUiState("selected video: ${video.asPath}")
}

class MediaViewModel(
    appPreferences: IAppPreferences,
    wsdk: Wsdk,
) : BaseConnectedViewModel(appPreferences, wsdk, "MediaViewModel") {
    private val _state = MutableStateFlow<MediaUiState>(MediaUiState.Error("not yet initialized"))
    val state = _state.asStateFlow()

    private val _mediaList = MutableStateFlow<List<MediaId>>(listOf())
    val mediaList = _mediaList.asStateFlow()


    fun getMediaList() {
        viewModelScope.launch {
            val mediaFileList = mutableListOf<MediaId>()
            gopro.commands.getMediaList().getOrThrow().run {
                this.media.forEach { mediaDirectory ->
                    mediaFileList += mediaDirectory.files.map {
                        MediaId(it.filename, mediaDirectory.directory)
                    }
                }
            }
            _mediaList.update { mediaFileList }
            _state.update { MediaUiState.Ready }
        }
    }

    fun getMedia(item: MediaId) {
        viewModelScope.launch {
            _state.update { MediaUiState.RetrievingMedia(item) }
            val metaData = gopro.commands.getMediaMetadata(item).getOrThrow()
            if (item.isPhoto) {
                val binary = gopro.commands.downloadMedia(item).getOrThrow()
                _state.update { MediaUiState.ActivePhoto(item, metaData, binary) }
            } else if (item.isVideo) {
                // TODO display from bytearray isn't working because we're having allocation failures.
                // probably need to write to disk. For now just show thumbnail
                // val binary = gopro.commands.downloadMedia(item).getOrThrow()
                val binary = gopro.commands.getThumbNail(item).getOrThrow()
                _state.update { MediaUiState.ActiveVideo(item, metaData, binary) }
            } else {
                throw Exception("${item.asPath} is not photo or video. Not currently handled.")
            }
        }
    }

    override fun onStart() {
        if (gopro.isHttpAvailable) {
            _state.update { MediaUiState.Ready }
        } else {
            _state.update { MediaUiState.Error("HTTP not available.") }
        }
    }
}