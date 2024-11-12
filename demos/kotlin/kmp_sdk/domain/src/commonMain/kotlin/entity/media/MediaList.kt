package entity.media

import entity.operation.MediaListItemSerializer
import entity.operation.StringAsBooleanSerializer
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

enum class GroupMediaItemType {
    @SerialName("b")
    BURST,

    @SerialName("c")
    CONTINUOUS,

    @SerialName("n")
    NIGHT_LAPSE,

    @SerialName("t")
    TIME_LAPSE
}

@Serializable(MediaListItemSerializer::class)
sealed class MediaListItem {
    @SerialName("n")
    abstract val filename: String

    @SerialName("cre")
    abstract val creationTime: Int

    @SerialName("mod")
    abstract val modifiedTime: Int

    @SerialName("s")
    abstract val fileSize: Int

    @SerialName("glrv")
    open val lowResVideoSize: Int? = null

    @SerialName("ls")
    open val lowResFileSize: Int? = null

    @SerialName("id")
    open val sessionId: String? = null

    @SerialName("raw")
    open val isRaw: Boolean? = null
}

@Serializable
data class SingleMediaListItem(
    @SerialName("n") override val filename: String,
    @SerialName("cre") override val creationTime: Int,
    @SerialName("mod") override val modifiedTime: Int,
    @SerialName("s") override val fileSize: Int,
    @SerialName("glrv") override val lowResVideoSize: Int? = null,
    @SerialName("ls") override val lowResFileSize: Int? = null,
    @SerialName("id") override val sessionId: String? = null,
    @Serializable(with = StringAsBooleanSerializer::class) @SerialName("raw") override val isRaw: Boolean? = null,
) : MediaListItem()

@Serializable
data class GroupedMediaListItem(
    @SerialName("n") override val filename: String,
    @SerialName("cre") override val creationTime: Int,
    @SerialName("mod") override val modifiedTime: Int,
    @SerialName("s") override val fileSize: Int,
    @SerialName("glrv") override val lowResVideoSize: Int? = null,
    @SerialName("ls") override val lowResFileSize: Int? = null,
    @SerialName("id") override val sessionId: String? = null,
    @Serializable(with = StringAsBooleanSerializer::class) @SerialName("raw") override val isRaw: Boolean? = null,

    @SerialName("g") val groupId: Int,
    @SerialName("b") val firstGroupMemberId: Int? = null,
    @SerialName("l") val lastGroupMemberId: Int? = null,
    @SerialName("m") val missingFileIds: List<Int>? = null,
    @SerialName("t") val groupType: GroupMediaItemType,
) : MediaListItem()

@Serializable
data class MediaFileList(
    @SerialName("d") val directory: String,
    @SerialName("fs") val files: List<MediaListItem>
)

@Serializable
data class MediaList(
    val id: String,
    val media: List<MediaFileList>
)