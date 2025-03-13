/* Media.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.Transient

@Serializable
data class MediaId(val filename: String, val folder: String) {
  val asPath: String
    get() = "$folder/$filename"

  val isPhoto: Boolean
    get() = filename.endsWith("jpg", ignoreCase = true)

  val isVideo: Boolean
    get() = filename.endsWith("mp4", ignoreCase = true)
}

enum class GroupMediaItemType {
  @SerialName("b") BURST,
  @SerialName("c") CONTINUOUS,
  @SerialName("n") NIGHT_LAPSE,
  @SerialName("t") TIME_LAPSE
}

@Serializable(MediaListItemSerializer::class)
sealed class MediaListItem {
  @SerialName("n") abstract val filename: String

  @SerialName("cre") abstract val creationTime: Int

  @SerialName("mod") abstract val modifiedTime: Int

  @SerialName("s") abstract val fileSize: Int

  @SerialName("glrv") open val lowResVideoSize: Int? = null

  @SerialName("ls") open val lowResFileSize: Int? = null

  @SerialName("id") open val sessionId: String? = null

  @SerialName("raw") open val isRaw: Boolean? = null
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
    @Serializable(with = StringAsBooleanSerializer::class)
    @SerialName("raw")
    override val isRaw: Boolean? = null,
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
    @Serializable(with = StringAsBooleanSerializer::class)
    @SerialName("raw")
    override val isRaw: Boolean? = null,
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

@Serializable data class MediaList(val id: String, val media: List<MediaFileList>)

enum class MediaContentType {
  @SerialName("0") VIDEO,
  @SerialName("1") LOOPING,
  @SerialName("2") CHAPTERED_VIDEO,
  @SerialName("3") TIME_LAPSE,
  @SerialName("4") SINGLE_PHOTO,
  @SerialName("5") BURST_PHOTO,
  @SerialName("6") TIME_LAPSE_PHOTO,
  @SerialName("8") NIGHT_LAPSE_PHOTO,
  @SerialName("9") NIGHT_PHOTO,
  @SerialName("10") CONTINUOUS_PHOTO,
  @SerialName("11") RAW_PHOTO,
  @SerialName("12") LIVE_BURST,
}

enum class AudioOption {
  @SerialName("auto") AUTO,
  @SerialName("wind") WIND,
  @SerialName("stereo") STEREO,
  @SerialName("off") OFF,
}

enum class OffloadState(val value: String) {
  APP("app"),
  PC("pc"),
  OTHER("other")
}

enum class LensConfig {
  @SerialName("0") FRONT,
  @SerialName("1") REAR
}

enum class LensProjection {
  @SerialName("0") EAC,
  @SerialName("1") ERP,
  @SerialName("2") EAC_SPLIT_HORIZ,
  @SerialName("3") ERP_CROPPED_PANO,
  @SerialName("4") ADJ_CIRCLES_NO_STITCH,
  @SerialName("5") OFFLINE_NO_STITCH,
  @SerialName("6") NO_STITCH,
  @SerialName("7") NO_EAC_SPLIT,
  @SerialName("8") HEMISPHERIC,
  @SerialName("9") ERROR,
}

@Serializable(MediaMetadataSerializer::class)
sealed class MediaMetadata {
  @SerialName("ct") abstract val contentType: MediaContentType

  @SerialName("cre") abstract val creationTime: Long

  @SerialName("s") abstract val fileSize: Int

  @SerialName("gumi") abstract val id: String

  @SerialName("h") abstract val height: Int

  @SerialName("w") abstract val width: Int

  @SerialName("hc") abstract val numHilights: Int

  @SerialName("eis")
  @Serializable(with = StringAsBooleanSerializer::class)
  abstract val isStabilized: Boolean

  @SerialName("mp")
  @Serializable(with = StringAsBooleanSerializer::class)
  abstract val isMetadataPresent: Boolean

  @Transient @SerialName("rot") open val deprecated: String? = null // deprecated

  @SerialName("tr")
  @Serializable(with = StringAsBooleanSerializer::class)
  abstract val isTranscoded: Boolean

  @SerialName("us")
  @Serializable(with = StringAsBooleanSerializer::class)
  abstract val isUploaded: Boolean

  @SerialName("mos") open val offloadState: List<OffloadState>? = null

  @SerialName("pgumi") open val parentId: String? = null

  open val fov: String? = null

  @SerialName("lc") open val lensConfig: LensConfig? = null

  @SerialName("prjn") open val lensProjection: LensProjection? = null
}

// TODO this inheritance is debatably useful. I can not find a way to inherit the SerialNames from:
// https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/polymorphism.md

@Serializable
data class VideoMediaMetadata(
    @SerialName("ct") override val contentType: MediaContentType,
    @SerialName("cre") override val creationTime: Long,
    @SerialName("s") override val fileSize: Int,
    @SerialName("gumi") override val id: String,
    @SerialName("h") override val height: Int,
    @SerialName("w") override val width: Int,
    @SerialName("hc") override val numHilights: Int,
    @SerialName("eis")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isStabilized: Boolean,
    @SerialName("mp")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isMetadataPresent: Boolean,
    @SerialName("tr")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isTranscoded: Boolean,
    @SerialName("us")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isUploaded: Boolean,
    @SerialName("mos") override val offloadState: List<OffloadState>? = null,
    @SerialName("pgumi") override val parentId: String? = null,
    override val fov: String? = null,
    @SerialName("lc") override val lensConfig: LensConfig? = null,
    @SerialName("prjn") override val lensProjection: LensProjection? = null,
    @SerialName("rot") override val deprecated: String? = null,
    @SerialName("ao") val audioOption: AudioOption,
    @SerialName("profile") val videoCodecLevel: Int,
    @SerialName("avc_profile") val videoCodecProfile: Int,
    @SerialName("cl") @Serializable(with = StringAsBooleanSerializer::class) val isClipped: Boolean,
    @SerialName("dur") val duration: Int,
    @SerialName("fps") val frameRate: Int,
    @SerialName("fps_denom") val frameRateDenominator: Int,
    @SerialName("hi") val hilightList: List<Int>,
    @SerialName("ls") val lrvFileSize: Int,
    @SerialName("pta")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isProtuneAudio: Boolean,
    @SerialName("subsample")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isSubsampled: Boolean,
    @SerialName("mahs") val maxAutoHilightScore: Int? = null,
    @SerialName("prog")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isProgressive: Boolean? = null
) : MediaMetadata()

@Serializable
data class PhotoMediaMetadata(
    @SerialName("ct") override val contentType: MediaContentType,
    @SerialName("cre") override val creationTime: Long,
    @SerialName("s") override val fileSize: Int,
    @SerialName("gumi") override val id: String,
    @SerialName("h") override val height: Int,
    @SerialName("w") override val width: Int,
    @SerialName("hc") override val numHilights: Int,
    @SerialName("eis")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isStabilized: Boolean,
    @SerialName("mp")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isMetadataPresent: Boolean,
    @SerialName("tr")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isTranscoded: Boolean,
    @SerialName("us")
    @Serializable(with = StringAsBooleanSerializer::class)
    override val isUploaded: Boolean,
    @SerialName("mos") override val offloadState: List<OffloadState>? = null,
    @SerialName("pgumi") override val parentId: String? = null,
    override val fov: String? = null,
    @SerialName("lc") override val lensConfig: LensConfig? = null,
    @SerialName("prjn") override val lensProjection: LensProjection? = null,
    @SerialName("rot") override val deprecated: String? = null,
    @SerialName("raw")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isRaw: Boolean? = null,
    @SerialName("wdr")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isWideDynamicRange: Boolean? = null,
    @SerialName("hdr")
    @Serializable(with = StringAsBooleanSerializer::class)
    val isHighDynamicRange: Boolean? = null,
) : MediaMetadata()
