package entity.media

import kotlinx.serialization.Serializable

@Serializable
data class MediaId(
    val filename: String,
    val folder: String
) {
    val asPath: String
        get() = "$folder/$filename"

    val isPhoto: Boolean
        get() = filename.endsWith("jpg", ignoreCase = true)

    val isVideo: Boolean
        get() = filename.endsWith("mp4", ignoreCase = true)
}