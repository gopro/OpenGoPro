package com.gopro.open_gopro.entity.operation

import entity.operation.proto.EnumFlatMode
import entity.operation.proto.EnumPresetGroup
import entity.operation.proto.EnumPresetGroupIcon
import entity.operation.proto.EnumPresetIcon
import entity.operation.proto.EnumPresetTitle
import kotlinx.serialization.Contextual
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

enum class PresetGroupId(val value: UInt) {
    VIDEO(1000U),
    PHOTO(1001U),
    TIMELAPSE(1002U);

    companion object {
        fun fromUInt(value: UInt) = entries.first { it.value == value }
    }
}

@Serializable
data class UpdateCustomPresetRequest(
    @SerialName("custom_name") val name: String? = null,
    @SerialName("icon_id") val iconId: Int? = null,
    @SerialName("title_id") val titleId: Int? = null
)

@Serializable
data class Range(
    val length: Int? = null,
    val start: Int? = null
)

@Serializable
data class PresetSetting(
    val id: Int? = null,
    val isCaption: Boolean? = null,
    val value: Int? = null
)

@Serializable
data class Preset(
    @Contextual val icon: EnumPresetIcon? = null,
    val id: Int? = null,
    val isFixed: Boolean? = null,
    val isModified: Boolean? = null,
    @Contextual val mode: EnumFlatMode? = null,
    @SerialName("settingArray") val settings: List<PresetSetting>? = null,
    @Contextual val titleId: EnumPresetTitle? = null,
    val titleNumber: Int? = null,
    @SerialName("userDefined") val isUserDefined: Boolean? = null,
    val customName: String? = null
)

@Serializable
data class PresetGroup(
    val canAddPreset: Boolean? = null,
    @Contextual val icon: EnumPresetGroupIcon? = null,
    @Contextual val id: EnumPresetGroup? = null,
    @SerialName("modeArray") val modes: List<@Contextual EnumFlatMode>? = null,
    @SerialName("presetArray") val presets: List<Preset>? = null
)

@Serializable
data class PresetInfo(
    val customIconIds: List<Range>? = null,
    val customTitleIds: List<Range>? = null,
    val presetGroupArray: List<PresetGroup>? = null
)

