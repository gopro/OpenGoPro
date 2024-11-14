package presenter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.touchlab.kermit.Logger
import data.IAppPreferences
import entity.media.MediaId
import entity.media.MediaMetadata
import gopro.GoPro
import gopro.IGoProFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class MediaUiState(val name: String) {
    data object Idle : MediaUiState("idle")
    data object WaitingMediaSelection : MediaUiState("waiting media selection")
    data class ActivePhoto(val photo: MediaId, val metadata: MediaMetadata, val data: ByteArray) :
        MediaUiState("selected photo: ${photo.asPath}")

    data class ActiveVideo(val video: MediaId, val metadata: MediaMetadata, val data: ByteArray) :
        MediaUiState("selected video: ${video.asPath}")
}

class MediaViewModel(
    private val appPreferences: IAppPreferences,
    private val goProFactory: IGoProFactory,
) : ViewModel() {
    private val logger = Logger.withTag("MediaViewModel")

    private lateinit var gopro: GoPro

    private val _state = MutableStateFlow<MediaUiState>(MediaUiState.Idle)
    val state = _state.asStateFlow()

    private val _mediaList = MutableStateFlow<List<MediaId>>(listOf())
    val mediaList = _mediaList.asStateFlow()


    fun getMediaList() {
        viewModelScope.launch {
            // TODO there's probably some functional operator for this
            val mediaFileList = mutableListOf<MediaId>()
            gopro.commands.getMediaList().getOrThrow().run {
                this.media.forEach { mediaDirectory ->
                    mediaFileList += mediaDirectory.files.map {
                        MediaId(it.filename, mediaDirectory.directory)
                    }
                }
            }
            _mediaList.update { mediaFileList }
            _state.update { MediaUiState.WaitingMediaSelection }
        }
    }

    fun getMedia(item: MediaId) {
        viewModelScope.launch {
            val metaData = gopro.commands.getMediaMetadata(item).getOrThrow()
            if (item.isPhoto) {
                val binary = gopro.commands.downloadMedia(item).getOrThrow()
                _state.update { MediaUiState.ActivePhoto(item, metaData, binary) }
            } else if (item.isVideo) {
                // TODO display from bytearray isn't working because we're having allocation failures.
                // TODO probably need to write to disk. For now just show thumbnail
                // val binary = gopro.commands.downloadMedia(item).getOrThrow()
                val binary = gopro.commands.getThumbNail(item).getOrThrow()
                _state.update { MediaUiState.ActiveVideo(item, metaData, binary) }
            } else {
                throw Exception("${item.asPath} is not photo or video. Not currently handled.")
            }
        }
    }

    fun start() {
        viewModelScope.launch {
            appPreferences.getConnectedDevice()?.let {
                gopro = goProFactory.getGoPro(it)
            } ?: throw Exception("No connected device found.")
        }
    }

    fun stop() {

    }
}