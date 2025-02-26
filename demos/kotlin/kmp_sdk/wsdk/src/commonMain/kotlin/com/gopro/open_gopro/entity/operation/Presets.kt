/* Presets.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

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

@Serializable data class Range(val length: Int? = null, val start: Int? = null)

@Serializable
data class WrappedPresetSetting(
    val id: Int? = null,
    val isCaption: Boolean? = null,
    val value: Int? = null
)

@Serializable
data class WrappedPreset(
    @Contextual val icon: EnumPresetIcon? = null,
    val id: Int? = null,
    val isFixed: Boolean? = null,
    val isModified: Boolean? = null,
    @Contextual val mode: EnumFlatMode? = null,
    @SerialName("settingArray") val settings: List<WrappedPresetSetting>? = null,
    @Contextual val titleId: EnumPresetTitle? = null,
    val titleNumber: Int? = null,
    @SerialName("userDefined") val isUserDefined: Boolean? = null,
    val customName: String? = null
)

@Serializable
data class WrappedPresetGroup(
    val canAddPreset: Boolean? = null,
    @Contextual val icon: EnumPresetGroupIcon? = null,
    @Contextual val id: EnumPresetGroup? = null,
    @SerialName("modeArray") val modes: List<@Contextual EnumFlatMode>? = null,
    @SerialName("presetArray") val presets: List<WrappedPreset>? = null
)

@Serializable
data class PresetInfo(
    val customIconIds: List<Range>? = null,
    val customTitleIds: List<Range>? = null,
    val presetGroupArray: List<WrappedPresetGroup>? = null
)
