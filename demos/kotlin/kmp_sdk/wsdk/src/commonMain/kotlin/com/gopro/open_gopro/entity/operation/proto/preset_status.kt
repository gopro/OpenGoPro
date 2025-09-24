/* preset_status.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
public sealed class EnumFlatMode(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumFlatMode && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumFlatMode.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object FLAT_MODE_UNKNOWN : EnumFlatMode(-1, "FLAT_MODE_UNKNOWN")

  internal object FLAT_MODE_PLAYBACK : EnumFlatMode(4, "FLAT_MODE_PLAYBACK")

  internal object FLAT_MODE_SETUP : EnumFlatMode(5, "FLAT_MODE_SETUP")

  internal object FLAT_MODE_VIDEO : EnumFlatMode(12, "FLAT_MODE_VIDEO")

  internal object FLAT_MODE_TIME_LAPSE_VIDEO : EnumFlatMode(13, "FLAT_MODE_TIME_LAPSE_VIDEO")

  internal object FLAT_MODE_LOOPING : EnumFlatMode(15, "FLAT_MODE_LOOPING")

  internal object FLAT_MODE_PHOTO_SINGLE : EnumFlatMode(16, "FLAT_MODE_PHOTO_SINGLE")

  internal object FLAT_MODE_PHOTO : EnumFlatMode(17, "FLAT_MODE_PHOTO")

  internal object FLAT_MODE_PHOTO_NIGHT : EnumFlatMode(18, "FLAT_MODE_PHOTO_NIGHT")

  internal object FLAT_MODE_PHOTO_BURST : EnumFlatMode(19, "FLAT_MODE_PHOTO_BURST")

  internal object FLAT_MODE_TIME_LAPSE_PHOTO : EnumFlatMode(20, "FLAT_MODE_TIME_LAPSE_PHOTO")

  internal object FLAT_MODE_NIGHT_LAPSE_PHOTO : EnumFlatMode(21, "FLAT_MODE_NIGHT_LAPSE_PHOTO")

  internal object FLAT_MODE_BROADCAST_RECORD : EnumFlatMode(22, "FLAT_MODE_BROADCAST_RECORD")

  internal object FLAT_MODE_BROADCAST_BROADCAST : EnumFlatMode(23, "FLAT_MODE_BROADCAST_BROADCAST")

  internal object FLAT_MODE_TIME_WARP_VIDEO : EnumFlatMode(24, "FLAT_MODE_TIME_WARP_VIDEO")

  internal object FLAT_MODE_LIVE_BURST : EnumFlatMode(25, "FLAT_MODE_LIVE_BURST")

  internal object FLAT_MODE_NIGHT_LAPSE_VIDEO : EnumFlatMode(26, "FLAT_MODE_NIGHT_LAPSE_VIDEO")

  internal object FLAT_MODE_SLOMO : EnumFlatMode(27, "FLAT_MODE_SLOMO")

  internal object FLAT_MODE_IDLE : EnumFlatMode(28, "FLAT_MODE_IDLE")

  internal object FLAT_MODE_VIDEO_STAR_TRAIL : EnumFlatMode(29, "FLAT_MODE_VIDEO_STAR_TRAIL")

  internal object FLAT_MODE_VIDEO_LIGHT_PAINTING :
      EnumFlatMode(30, "FLAT_MODE_VIDEO_LIGHT_PAINTING")

  internal object FLAT_MODE_VIDEO_LIGHT_TRAIL : EnumFlatMode(31, "FLAT_MODE_VIDEO_LIGHT_TRAIL")

  internal object FLAT_MODE_VIDEO_BURST_SLOMO : EnumFlatMode(32, "FLAT_MODE_VIDEO_BURST_SLOMO")

  internal class UNRECOGNIZED(value: Int) : EnumFlatMode(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumFlatMode> {
    internal val values: List<com.gopro.open_gopro.operations.EnumFlatMode> by lazy {
      listOf(
          FLAT_MODE_UNKNOWN,
          FLAT_MODE_PLAYBACK,
          FLAT_MODE_SETUP,
          FLAT_MODE_VIDEO,
          FLAT_MODE_TIME_LAPSE_VIDEO,
          FLAT_MODE_LOOPING,
          FLAT_MODE_PHOTO_SINGLE,
          FLAT_MODE_PHOTO,
          FLAT_MODE_PHOTO_NIGHT,
          FLAT_MODE_PHOTO_BURST,
          FLAT_MODE_TIME_LAPSE_PHOTO,
          FLAT_MODE_NIGHT_LAPSE_PHOTO,
          FLAT_MODE_BROADCAST_RECORD,
          FLAT_MODE_BROADCAST_BROADCAST,
          FLAT_MODE_TIME_WARP_VIDEO,
          FLAT_MODE_LIVE_BURST,
          FLAT_MODE_NIGHT_LAPSE_VIDEO,
          FLAT_MODE_SLOMO,
          FLAT_MODE_IDLE,
          FLAT_MODE_VIDEO_STAR_TRAIL,
          FLAT_MODE_VIDEO_LIGHT_PAINTING,
          FLAT_MODE_VIDEO_LIGHT_TRAIL,
          FLAT_MODE_VIDEO_BURST_SLOMO)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumFlatMode =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumFlatMode =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumFlatMode with name: $name")
  }
}

@pbandk.Export
public sealed class EnumPresetGroup(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumPresetGroup && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumPresetGroup.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object PRESET_GROUP_ID_VIDEO : EnumPresetGroup(1000, "PRESET_GROUP_ID_VIDEO")

  internal object PRESET_GROUP_ID_PHOTO : EnumPresetGroup(1001, "PRESET_GROUP_ID_PHOTO")

  internal object PRESET_GROUP_ID_TIMELAPSE : EnumPresetGroup(1002, "PRESET_GROUP_ID_TIMELAPSE")

  internal class UNRECOGNIZED(value: Int) : EnumPresetGroup(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPresetGroup> {
    internal val values: List<com.gopro.open_gopro.operations.EnumPresetGroup> by lazy {
      listOf(PRESET_GROUP_ID_VIDEO, PRESET_GROUP_ID_PHOTO, PRESET_GROUP_ID_TIMELAPSE)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPresetGroup =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPresetGroup =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumPresetGroup with name: $name")
  }
}

@pbandk.Export
public sealed class EnumPresetGroupIcon(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumPresetGroupIcon && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumPresetGroupIcon.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object PRESET_GROUP_VIDEO_ICON_ID : EnumPresetGroupIcon(0, "PRESET_GROUP_VIDEO_ICON_ID")

  internal object PRESET_GROUP_PHOTO_ICON_ID : EnumPresetGroupIcon(1, "PRESET_GROUP_PHOTO_ICON_ID")

  internal object PRESET_GROUP_TIMELAPSE_ICON_ID :
      EnumPresetGroupIcon(2, "PRESET_GROUP_TIMELAPSE_ICON_ID")

  internal object PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID :
      EnumPresetGroupIcon(3, "PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID")

  internal object PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID :
      EnumPresetGroupIcon(4, "PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID")

  internal object PRESET_GROUP_MAX_VIDEO_ICON_ID :
      EnumPresetGroupIcon(5, "PRESET_GROUP_MAX_VIDEO_ICON_ID")

  internal object PRESET_GROUP_MAX_PHOTO_ICON_ID :
      EnumPresetGroupIcon(6, "PRESET_GROUP_MAX_PHOTO_ICON_ID")

  internal object PRESET_GROUP_MAX_TIMELAPSE_ICON_ID :
      EnumPresetGroupIcon(7, "PRESET_GROUP_MAX_TIMELAPSE_ICON_ID")

  internal object PRESET_GROUP_ND_MOD_VIDEO_ICON_ID :
      EnumPresetGroupIcon(8, "PRESET_GROUP_ND_MOD_VIDEO_ICON_ID")

  internal object PRESET_GROUP_ND_MOD_PHOTO_ICON_ID :
      EnumPresetGroupIcon(9, "PRESET_GROUP_ND_MOD_PHOTO_ICON_ID")

  internal object PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID :
      EnumPresetGroupIcon(10, "PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID")

  internal class UNRECOGNIZED(value: Int) : EnumPresetGroupIcon(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPresetGroupIcon> {
    internal val values: List<com.gopro.open_gopro.operations.EnumPresetGroupIcon> by lazy {
      listOf(
          PRESET_GROUP_VIDEO_ICON_ID,
          PRESET_GROUP_PHOTO_ICON_ID,
          PRESET_GROUP_TIMELAPSE_ICON_ID,
          PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID,
          PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID,
          PRESET_GROUP_MAX_VIDEO_ICON_ID,
          PRESET_GROUP_MAX_PHOTO_ICON_ID,
          PRESET_GROUP_MAX_TIMELAPSE_ICON_ID,
          PRESET_GROUP_ND_MOD_VIDEO_ICON_ID,
          PRESET_GROUP_ND_MOD_PHOTO_ICON_ID,
          PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPresetGroupIcon =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPresetGroupIcon =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumPresetGroupIcon with name: $name")
  }
}

@pbandk.Export
public sealed class EnumPresetIcon(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumPresetIcon && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumPresetIcon.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object PRESET_ICON_VIDEO : EnumPresetIcon(0, "PRESET_ICON_VIDEO")

  internal object PRESET_ICON_ACTIVITY : EnumPresetIcon(1, "PRESET_ICON_ACTIVITY")

  internal object PRESET_ICON_CINEMATIC : EnumPresetIcon(2, "PRESET_ICON_CINEMATIC")

  internal object PRESET_ICON_PHOTO : EnumPresetIcon(3, "PRESET_ICON_PHOTO")

  internal object PRESET_ICON_LIVE_BURST : EnumPresetIcon(4, "PRESET_ICON_LIVE_BURST")

  internal object PRESET_ICON_BURST : EnumPresetIcon(5, "PRESET_ICON_BURST")

  internal object PRESET_ICON_PHOTO_NIGHT : EnumPresetIcon(6, "PRESET_ICON_PHOTO_NIGHT")

  internal object PRESET_ICON_TIMEWARP : EnumPresetIcon(7, "PRESET_ICON_TIMEWARP")

  internal object PRESET_ICON_TIMELAPSE : EnumPresetIcon(8, "PRESET_ICON_TIMELAPSE")

  internal object PRESET_ICON_NIGHTLAPSE : EnumPresetIcon(9, "PRESET_ICON_NIGHTLAPSE")

  internal object PRESET_ICON_SNAIL : EnumPresetIcon(10, "PRESET_ICON_SNAIL")

  internal object PRESET_ICON_VIDEO_2 : EnumPresetIcon(11, "PRESET_ICON_VIDEO_2")

  internal object PRESET_ICON_PHOTO_2 : EnumPresetIcon(13, "PRESET_ICON_PHOTO_2")

  internal object PRESET_ICON_PANORAMA : EnumPresetIcon(14, "PRESET_ICON_PANORAMA")

  internal object PRESET_ICON_BURST_2 : EnumPresetIcon(15, "PRESET_ICON_BURST_2")

  internal object PRESET_ICON_TIMEWARP_2 : EnumPresetIcon(16, "PRESET_ICON_TIMEWARP_2")

  internal object PRESET_ICON_TIMELAPSE_2 : EnumPresetIcon(17, "PRESET_ICON_TIMELAPSE_2")

  internal object PRESET_ICON_CUSTOM : EnumPresetIcon(18, "PRESET_ICON_CUSTOM")

  internal object PRESET_ICON_AIR : EnumPresetIcon(19, "PRESET_ICON_AIR")

  internal object PRESET_ICON_BIKE : EnumPresetIcon(20, "PRESET_ICON_BIKE")

  internal object PRESET_ICON_EPIC : EnumPresetIcon(21, "PRESET_ICON_EPIC")

  internal object PRESET_ICON_INDOOR : EnumPresetIcon(22, "PRESET_ICON_INDOOR")

  internal object PRESET_ICON_MOTOR : EnumPresetIcon(23, "PRESET_ICON_MOTOR")

  internal object PRESET_ICON_MOUNTED : EnumPresetIcon(24, "PRESET_ICON_MOUNTED")

  internal object PRESET_ICON_OUTDOOR : EnumPresetIcon(25, "PRESET_ICON_OUTDOOR")

  internal object PRESET_ICON_POV : EnumPresetIcon(26, "PRESET_ICON_POV")

  internal object PRESET_ICON_SELFIE : EnumPresetIcon(27, "PRESET_ICON_SELFIE")

  internal object PRESET_ICON_SKATE : EnumPresetIcon(28, "PRESET_ICON_SKATE")

  internal object PRESET_ICON_SNOW : EnumPresetIcon(29, "PRESET_ICON_SNOW")

  internal object PRESET_ICON_TRAIL : EnumPresetIcon(30, "PRESET_ICON_TRAIL")

  internal object PRESET_ICON_TRAVEL : EnumPresetIcon(31, "PRESET_ICON_TRAVEL")

  internal object PRESET_ICON_WATER : EnumPresetIcon(32, "PRESET_ICON_WATER")

  internal object PRESET_ICON_LOOPING : EnumPresetIcon(33, "PRESET_ICON_LOOPING")

  internal object PRESET_ICON_STARS : EnumPresetIcon(34, "PRESET_ICON_STARS")

  internal object PRESET_ICON_ACTION : EnumPresetIcon(35, "PRESET_ICON_ACTION")

  internal object PRESET_ICON_FOLLOW_CAM : EnumPresetIcon(36, "PRESET_ICON_FOLLOW_CAM")

  internal object PRESET_ICON_SURF : EnumPresetIcon(37, "PRESET_ICON_SURF")

  internal object PRESET_ICON_CITY : EnumPresetIcon(38, "PRESET_ICON_CITY")

  internal object PRESET_ICON_SHAKY : EnumPresetIcon(39, "PRESET_ICON_SHAKY")

  internal object PRESET_ICON_CHESTY : EnumPresetIcon(40, "PRESET_ICON_CHESTY")

  internal object PRESET_ICON_HELMET : EnumPresetIcon(41, "PRESET_ICON_HELMET")

  internal object PRESET_ICON_BITE : EnumPresetIcon(42, "PRESET_ICON_BITE")

  internal object PRESET_ICON_CUSTOM_CINEMATIC : EnumPresetIcon(43, "PRESET_ICON_CUSTOM_CINEMATIC")

  internal object PRESET_ICON_VLOG : EnumPresetIcon(44, "PRESET_ICON_VLOG")

  internal object PRESET_ICON_FPV : EnumPresetIcon(45, "PRESET_ICON_FPV")

  internal object PRESET_ICON_HDR : EnumPresetIcon(46, "PRESET_ICON_HDR")

  internal object PRESET_ICON_LANDSCAPE : EnumPresetIcon(47, "PRESET_ICON_LANDSCAPE")

  internal object PRESET_ICON_LOG : EnumPresetIcon(48, "PRESET_ICON_LOG")

  internal object PRESET_ICON_CUSTOM_SLOMO : EnumPresetIcon(49, "PRESET_ICON_CUSTOM_SLOMO")

  internal object PRESET_ICON_TRIPOD : EnumPresetIcon(50, "PRESET_ICON_TRIPOD")

  internal object PRESET_ICON_MAX_VIDEO : EnumPresetIcon(55, "PRESET_ICON_MAX_VIDEO")

  internal object PRESET_ICON_MAX_PHOTO : EnumPresetIcon(56, "PRESET_ICON_MAX_PHOTO")

  internal object PRESET_ICON_MAX_TIMEWARP : EnumPresetIcon(57, "PRESET_ICON_MAX_TIMEWARP")

  internal object PRESET_ICON_BASIC : EnumPresetIcon(58, "PRESET_ICON_BASIC")

  internal object PRESET_ICON_ULTRA_SLO_MO : EnumPresetIcon(59, "PRESET_ICON_ULTRA_SLO_MO")

  internal object PRESET_ICON_STANDARD_ENDURANCE :
      EnumPresetIcon(60, "PRESET_ICON_STANDARD_ENDURANCE")

  internal object PRESET_ICON_ACTIVITY_ENDURANCE :
      EnumPresetIcon(61, "PRESET_ICON_ACTIVITY_ENDURANCE")

  internal object PRESET_ICON_CINEMATIC_ENDURANCE :
      EnumPresetIcon(62, "PRESET_ICON_CINEMATIC_ENDURANCE")

  internal object PRESET_ICON_SLOMO_ENDURANCE : EnumPresetIcon(63, "PRESET_ICON_SLOMO_ENDURANCE")

  internal object PRESET_ICON_STATIONARY_1 : EnumPresetIcon(64, "PRESET_ICON_STATIONARY_1")

  internal object PRESET_ICON_STATIONARY_2 : EnumPresetIcon(65, "PRESET_ICON_STATIONARY_2")

  internal object PRESET_ICON_STATIONARY_3 : EnumPresetIcon(66, "PRESET_ICON_STATIONARY_3")

  internal object PRESET_ICON_STATIONARY_4 : EnumPresetIcon(67, "PRESET_ICON_STATIONARY_4")

  internal object PRESET_ICON_SIMPLE_SUPER_PHOTO :
      EnumPresetIcon(70, "PRESET_ICON_SIMPLE_SUPER_PHOTO")

  internal object PRESET_ICON_SIMPLE_NIGHT_PHOTO :
      EnumPresetIcon(71, "PRESET_ICON_SIMPLE_NIGHT_PHOTO")

  internal object PRESET_ICON_HIGHEST_QUALITY_VIDEO :
      EnumPresetIcon(73, "PRESET_ICON_HIGHEST_QUALITY_VIDEO")

  internal object PRESET_ICON_STANDARD_QUALITY_VIDEO :
      EnumPresetIcon(74, "PRESET_ICON_STANDARD_QUALITY_VIDEO")

  internal object PRESET_ICON_BASIC_QUALITY_VIDEO :
      EnumPresetIcon(75, "PRESET_ICON_BASIC_QUALITY_VIDEO")

  internal object PRESET_ICON_STAR_TRAIL : EnumPresetIcon(76, "PRESET_ICON_STAR_TRAIL")

  internal object PRESET_ICON_LIGHT_PAINTING : EnumPresetIcon(77, "PRESET_ICON_LIGHT_PAINTING")

  internal object PRESET_ICON_LIGHT_TRAIL : EnumPresetIcon(78, "PRESET_ICON_LIGHT_TRAIL")

  internal object PRESET_ICON_FULL_FRAME : EnumPresetIcon(79, "PRESET_ICON_FULL_FRAME")

  internal object PRESET_ICON_EASY_MAX_VIDEO : EnumPresetIcon(80, "PRESET_ICON_EASY_MAX_VIDEO")

  internal object PRESET_ICON_EASY_MAX_PHOTO : EnumPresetIcon(81, "PRESET_ICON_EASY_MAX_PHOTO")

  internal object PRESET_ICON_EASY_MAX_TIMEWARP :
      EnumPresetIcon(82, "PRESET_ICON_EASY_MAX_TIMEWARP")

  internal object PRESET_ICON_EASY_MAX_STAR_TRAIL :
      EnumPresetIcon(83, "PRESET_ICON_EASY_MAX_STAR_TRAIL")

  internal object PRESET_ICON_EASY_MAX_LIGHT_PAINTING :
      EnumPresetIcon(84, "PRESET_ICON_EASY_MAX_LIGHT_PAINTING")

  internal object PRESET_ICON_EASY_MAX_LIGHT_TRAIL :
      EnumPresetIcon(85, "PRESET_ICON_EASY_MAX_LIGHT_TRAIL")

  internal object PRESET_ICON_MAX_STAR_TRAIL : EnumPresetIcon(89, "PRESET_ICON_MAX_STAR_TRAIL")

  internal object PRESET_ICON_MAX_LIGHT_PAINTING :
      EnumPresetIcon(90, "PRESET_ICON_MAX_LIGHT_PAINTING")

  internal object PRESET_ICON_MAX_LIGHT_TRAIL : EnumPresetIcon(91, "PRESET_ICON_MAX_LIGHT_TRAIL")

  internal object PRESET_ICON_EASY_STANDARD_PROFILE :
      EnumPresetIcon(100, "PRESET_ICON_EASY_STANDARD_PROFILE")

  internal object PRESET_ICON_EASY_HDR_PROFILE :
      EnumPresetIcon(101, "PRESET_ICON_EASY_HDR_PROFILE")

  internal object PRESET_ICON_BURST_SLOMO : EnumPresetIcon(102, "PRESET_ICON_BURST_SLOMO")

  internal object PRESET_ICON_TIMELAPSE_PHOTO : EnumPresetIcon(1000, "PRESET_ICON_TIMELAPSE_PHOTO")

  internal object PRESET_ICON_NIGHTLAPSE_PHOTO :
      EnumPresetIcon(1001, "PRESET_ICON_NIGHTLAPSE_PHOTO")

  internal class UNRECOGNIZED(value: Int) : EnumPresetIcon(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPresetIcon> {
    internal val values: List<com.gopro.open_gopro.operations.EnumPresetIcon> by lazy {
      listOf(
          PRESET_ICON_VIDEO,
          PRESET_ICON_ACTIVITY,
          PRESET_ICON_CINEMATIC,
          PRESET_ICON_PHOTO,
          PRESET_ICON_LIVE_BURST,
          PRESET_ICON_BURST,
          PRESET_ICON_PHOTO_NIGHT,
          PRESET_ICON_TIMEWARP,
          PRESET_ICON_TIMELAPSE,
          PRESET_ICON_NIGHTLAPSE,
          PRESET_ICON_SNAIL,
          PRESET_ICON_VIDEO_2,
          PRESET_ICON_PHOTO_2,
          PRESET_ICON_PANORAMA,
          PRESET_ICON_BURST_2,
          PRESET_ICON_TIMEWARP_2,
          PRESET_ICON_TIMELAPSE_2,
          PRESET_ICON_CUSTOM,
          PRESET_ICON_AIR,
          PRESET_ICON_BIKE,
          PRESET_ICON_EPIC,
          PRESET_ICON_INDOOR,
          PRESET_ICON_MOTOR,
          PRESET_ICON_MOUNTED,
          PRESET_ICON_OUTDOOR,
          PRESET_ICON_POV,
          PRESET_ICON_SELFIE,
          PRESET_ICON_SKATE,
          PRESET_ICON_SNOW,
          PRESET_ICON_TRAIL,
          PRESET_ICON_TRAVEL,
          PRESET_ICON_WATER,
          PRESET_ICON_LOOPING,
          PRESET_ICON_STARS,
          PRESET_ICON_ACTION,
          PRESET_ICON_FOLLOW_CAM,
          PRESET_ICON_SURF,
          PRESET_ICON_CITY,
          PRESET_ICON_SHAKY,
          PRESET_ICON_CHESTY,
          PRESET_ICON_HELMET,
          PRESET_ICON_BITE,
          PRESET_ICON_CUSTOM_CINEMATIC,
          PRESET_ICON_VLOG,
          PRESET_ICON_FPV,
          PRESET_ICON_HDR,
          PRESET_ICON_LANDSCAPE,
          PRESET_ICON_LOG,
          PRESET_ICON_CUSTOM_SLOMO,
          PRESET_ICON_TRIPOD,
          PRESET_ICON_MAX_VIDEO,
          PRESET_ICON_MAX_PHOTO,
          PRESET_ICON_MAX_TIMEWARP,
          PRESET_ICON_BASIC,
          PRESET_ICON_ULTRA_SLO_MO,
          PRESET_ICON_STANDARD_ENDURANCE,
          PRESET_ICON_ACTIVITY_ENDURANCE,
          PRESET_ICON_CINEMATIC_ENDURANCE,
          PRESET_ICON_SLOMO_ENDURANCE,
          PRESET_ICON_STATIONARY_1,
          PRESET_ICON_STATIONARY_2,
          PRESET_ICON_STATIONARY_3,
          PRESET_ICON_STATIONARY_4,
          PRESET_ICON_SIMPLE_SUPER_PHOTO,
          PRESET_ICON_SIMPLE_NIGHT_PHOTO,
          PRESET_ICON_HIGHEST_QUALITY_VIDEO,
          PRESET_ICON_STANDARD_QUALITY_VIDEO,
          PRESET_ICON_BASIC_QUALITY_VIDEO,
          PRESET_ICON_STAR_TRAIL,
          PRESET_ICON_LIGHT_PAINTING,
          PRESET_ICON_LIGHT_TRAIL,
          PRESET_ICON_FULL_FRAME,
          PRESET_ICON_EASY_MAX_VIDEO,
          PRESET_ICON_EASY_MAX_PHOTO,
          PRESET_ICON_EASY_MAX_TIMEWARP,
          PRESET_ICON_EASY_MAX_STAR_TRAIL,
          PRESET_ICON_EASY_MAX_LIGHT_PAINTING,
          PRESET_ICON_EASY_MAX_LIGHT_TRAIL,
          PRESET_ICON_MAX_STAR_TRAIL,
          PRESET_ICON_MAX_LIGHT_PAINTING,
          PRESET_ICON_MAX_LIGHT_TRAIL,
          PRESET_ICON_EASY_STANDARD_PROFILE,
          PRESET_ICON_EASY_HDR_PROFILE,
          PRESET_ICON_BURST_SLOMO,
          PRESET_ICON_TIMELAPSE_PHOTO,
          PRESET_ICON_NIGHTLAPSE_PHOTO)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPresetIcon =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPresetIcon =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumPresetIcon with name: $name")
  }
}

@pbandk.Export
public sealed class EnumPresetTitle(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumPresetTitle && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumPresetTitle.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object PRESET_TITLE_ACTIVITY : EnumPresetTitle(0, "PRESET_TITLE_ACTIVITY")

  internal object PRESET_TITLE_STANDARD : EnumPresetTitle(1, "PRESET_TITLE_STANDARD")

  internal object PRESET_TITLE_CINEMATIC : EnumPresetTitle(2, "PRESET_TITLE_CINEMATIC")

  internal object PRESET_TITLE_PHOTO : EnumPresetTitle(3, "PRESET_TITLE_PHOTO")

  internal object PRESET_TITLE_LIVE_BURST : EnumPresetTitle(4, "PRESET_TITLE_LIVE_BURST")

  internal object PRESET_TITLE_BURST : EnumPresetTitle(5, "PRESET_TITLE_BURST")

  internal object PRESET_TITLE_NIGHT : EnumPresetTitle(6, "PRESET_TITLE_NIGHT")

  internal object PRESET_TITLE_TIME_WARP : EnumPresetTitle(7, "PRESET_TITLE_TIME_WARP")

  internal object PRESET_TITLE_TIME_LAPSE : EnumPresetTitle(8, "PRESET_TITLE_TIME_LAPSE")

  internal object PRESET_TITLE_NIGHT_LAPSE : EnumPresetTitle(9, "PRESET_TITLE_NIGHT_LAPSE")

  internal object PRESET_TITLE_VIDEO : EnumPresetTitle(10, "PRESET_TITLE_VIDEO")

  internal object PRESET_TITLE_SLOMO : EnumPresetTitle(11, "PRESET_TITLE_SLOMO")

  internal object PRESET_TITLE_PHOTO_2 : EnumPresetTitle(13, "PRESET_TITLE_PHOTO_2")

  internal object PRESET_TITLE_PANORAMA : EnumPresetTitle(14, "PRESET_TITLE_PANORAMA")

  internal object PRESET_TITLE_TIME_WARP_2 : EnumPresetTitle(16, "PRESET_TITLE_TIME_WARP_2")

  internal object PRESET_TITLE_CUSTOM : EnumPresetTitle(18, "PRESET_TITLE_CUSTOM")

  internal object PRESET_TITLE_AIR : EnumPresetTitle(19, "PRESET_TITLE_AIR")

  internal object PRESET_TITLE_BIKE : EnumPresetTitle(20, "PRESET_TITLE_BIKE")

  internal object PRESET_TITLE_EPIC : EnumPresetTitle(21, "PRESET_TITLE_EPIC")

  internal object PRESET_TITLE_INDOOR : EnumPresetTitle(22, "PRESET_TITLE_INDOOR")

  internal object PRESET_TITLE_MOTOR : EnumPresetTitle(23, "PRESET_TITLE_MOTOR")

  internal object PRESET_TITLE_MOUNTED : EnumPresetTitle(24, "PRESET_TITLE_MOUNTED")

  internal object PRESET_TITLE_OUTDOOR : EnumPresetTitle(25, "PRESET_TITLE_OUTDOOR")

  internal object PRESET_TITLE_POV : EnumPresetTitle(26, "PRESET_TITLE_POV")

  internal object PRESET_TITLE_SELFIE : EnumPresetTitle(27, "PRESET_TITLE_SELFIE")

  internal object PRESET_TITLE_SKATE : EnumPresetTitle(28, "PRESET_TITLE_SKATE")

  internal object PRESET_TITLE_SNOW : EnumPresetTitle(29, "PRESET_TITLE_SNOW")

  internal object PRESET_TITLE_TRAIL : EnumPresetTitle(30, "PRESET_TITLE_TRAIL")

  internal object PRESET_TITLE_TRAVEL : EnumPresetTitle(31, "PRESET_TITLE_TRAVEL")

  internal object PRESET_TITLE_WATER : EnumPresetTitle(32, "PRESET_TITLE_WATER")

  internal object PRESET_TITLE_LOOPING : EnumPresetTitle(33, "PRESET_TITLE_LOOPING")

  internal object PRESET_TITLE_STARS : EnumPresetTitle(34, "PRESET_TITLE_STARS")

  internal object PRESET_TITLE_ACTION : EnumPresetTitle(35, "PRESET_TITLE_ACTION")

  internal object PRESET_TITLE_FOLLOW_CAM : EnumPresetTitle(36, "PRESET_TITLE_FOLLOW_CAM")

  internal object PRESET_TITLE_SURF : EnumPresetTitle(37, "PRESET_TITLE_SURF")

  internal object PRESET_TITLE_CITY : EnumPresetTitle(38, "PRESET_TITLE_CITY")

  internal object PRESET_TITLE_SHAKY : EnumPresetTitle(39, "PRESET_TITLE_SHAKY")

  internal object PRESET_TITLE_CHESTY : EnumPresetTitle(40, "PRESET_TITLE_CHESTY")

  internal object PRESET_TITLE_HELMET : EnumPresetTitle(41, "PRESET_TITLE_HELMET")

  internal object PRESET_TITLE_BITE : EnumPresetTitle(42, "PRESET_TITLE_BITE")

  internal object PRESET_TITLE_CUSTOM_CINEMATIC :
      EnumPresetTitle(43, "PRESET_TITLE_CUSTOM_CINEMATIC")

  internal object PRESET_TITLE_VLOG : EnumPresetTitle(44, "PRESET_TITLE_VLOG")

  internal object PRESET_TITLE_FPV : EnumPresetTitle(45, "PRESET_TITLE_FPV")

  internal object PRESET_TITLE_HDR : EnumPresetTitle(46, "PRESET_TITLE_HDR")

  internal object PRESET_TITLE_LANDSCAPE : EnumPresetTitle(47, "PRESET_TITLE_LANDSCAPE")

  internal object PRESET_TITLE_LOG : EnumPresetTitle(48, "PRESET_TITLE_LOG")

  internal object PRESET_TITLE_CUSTOM_SLOMO : EnumPresetTitle(49, "PRESET_TITLE_CUSTOM_SLOMO")

  internal object PRESET_TITLE_TRIPOD : EnumPresetTitle(50, "PRESET_TITLE_TRIPOD")

  internal object PRESET_TITLE_BASIC : EnumPresetTitle(58, "PRESET_TITLE_BASIC")

  internal object PRESET_TITLE_ULTRA_SLO_MO : EnumPresetTitle(59, "PRESET_TITLE_ULTRA_SLO_MO")

  internal object PRESET_TITLE_STANDARD_ENDURANCE :
      EnumPresetTitle(60, "PRESET_TITLE_STANDARD_ENDURANCE")

  internal object PRESET_TITLE_ACTIVITY_ENDURANCE :
      EnumPresetTitle(61, "PRESET_TITLE_ACTIVITY_ENDURANCE")

  internal object PRESET_TITLE_CINEMATIC_ENDURANCE :
      EnumPresetTitle(62, "PRESET_TITLE_CINEMATIC_ENDURANCE")

  internal object PRESET_TITLE_SLOMO_ENDURANCE :
      EnumPresetTitle(63, "PRESET_TITLE_SLOMO_ENDURANCE")

  internal object PRESET_TITLE_STATIONARY_1 : EnumPresetTitle(64, "PRESET_TITLE_STATIONARY_1")

  internal object PRESET_TITLE_STATIONARY_2 : EnumPresetTitle(65, "PRESET_TITLE_STATIONARY_2")

  internal object PRESET_TITLE_STATIONARY_3 : EnumPresetTitle(66, "PRESET_TITLE_STATIONARY_3")

  internal object PRESET_TITLE_STATIONARY_4 : EnumPresetTitle(67, "PRESET_TITLE_STATIONARY_4")

  internal object PRESET_TITLE_SIMPLE_VIDEO : EnumPresetTitle(68, "PRESET_TITLE_SIMPLE_VIDEO")

  internal object PRESET_TITLE_SIMPLE_TIME_WARP :
      EnumPresetTitle(69, "PRESET_TITLE_SIMPLE_TIME_WARP")

  internal object PRESET_TITLE_SIMPLE_SUPER_PHOTO :
      EnumPresetTitle(70, "PRESET_TITLE_SIMPLE_SUPER_PHOTO")

  internal object PRESET_TITLE_SIMPLE_NIGHT_PHOTO :
      EnumPresetTitle(71, "PRESET_TITLE_SIMPLE_NIGHT_PHOTO")

  internal object PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE :
      EnumPresetTitle(72, "PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE")

  internal object PRESET_TITLE_HIGHEST_QUALITY :
      EnumPresetTitle(73, "PRESET_TITLE_HIGHEST_QUALITY")

  internal object PRESET_TITLE_EXTENDED_BATTERY :
      EnumPresetTitle(74, "PRESET_TITLE_EXTENDED_BATTERY")

  internal object PRESET_TITLE_LONGEST_BATTERY :
      EnumPresetTitle(75, "PRESET_TITLE_LONGEST_BATTERY")

  internal object PRESET_TITLE_STAR_TRAIL : EnumPresetTitle(76, "PRESET_TITLE_STAR_TRAIL")

  internal object PRESET_TITLE_LIGHT_PAINTING : EnumPresetTitle(77, "PRESET_TITLE_LIGHT_PAINTING")

  internal object PRESET_TITLE_LIGHT_TRAIL : EnumPresetTitle(78, "PRESET_TITLE_LIGHT_TRAIL")

  internal object PRESET_TITLE_FULL_FRAME : EnumPresetTitle(79, "PRESET_TITLE_FULL_FRAME")

  internal object PRESET_TITLE_STANDARD_QUALITY_VIDEO :
      EnumPresetTitle(82, "PRESET_TITLE_STANDARD_QUALITY_VIDEO")

  internal object PRESET_TITLE_BASIC_QUALITY_VIDEO :
      EnumPresetTitle(83, "PRESET_TITLE_BASIC_QUALITY_VIDEO")

  internal object PRESET_TITLE_HIGHEST_QUALITY_VIDEO :
      EnumPresetTitle(93, "PRESET_TITLE_HIGHEST_QUALITY_VIDEO")

  internal object PRESET_TITLE_USER_DEFINED_CUSTOM_NAME :
      EnumPresetTitle(94, "PRESET_TITLE_USER_DEFINED_CUSTOM_NAME")

  internal object PRESET_TITLE_EASY_STANDARD_PROFILE :
      EnumPresetTitle(99, "PRESET_TITLE_EASY_STANDARD_PROFILE")

  internal object PRESET_TITLE_EASY_HDR_PROFILE :
      EnumPresetTitle(100, "PRESET_TITLE_EASY_HDR_PROFILE")

  internal object PRESET_TITLE_BURST_SLOMO : EnumPresetTitle(106, "PRESET_TITLE_BURST_SLOMO")

  internal object PRESET_TITLE_4_3_VIDEO : EnumPresetTitle(125, "PRESET_TITLE_4_3_VIDEO")

  internal object PRESET_TITLE_16_9_VIDEO : EnumPresetTitle(126, "PRESET_TITLE_16_9_VIDEO")

  internal object PRESET_TITLE_16_9_SLOMO : EnumPresetTitle(127, "PRESET_TITLE_16_9_SLOMO")

  internal object PRESET_TITLE_TIME_LAPSE_VIDEO :
      EnumPresetTitle(131, "PRESET_TITLE_TIME_LAPSE_VIDEO")

  internal object PRESET_TITLE_TIME_LAPSE_PHOTO :
      EnumPresetTitle(132, "PRESET_TITLE_TIME_LAPSE_PHOTO")

  internal object PRESET_TITLE_NIGHT_LAPSE_VIDEO :
      EnumPresetTitle(133, "PRESET_TITLE_NIGHT_LAPSE_VIDEO")

  internal object PRESET_TITLE_NIGHT_LAPSE_PHOTO :
      EnumPresetTitle(134, "PRESET_TITLE_NIGHT_LAPSE_PHOTO")

  internal class UNRECOGNIZED(value: Int) : EnumPresetTitle(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPresetTitle> {
    internal val values: List<com.gopro.open_gopro.operations.EnumPresetTitle> by lazy {
      listOf(
          PRESET_TITLE_ACTIVITY,
          PRESET_TITLE_STANDARD,
          PRESET_TITLE_CINEMATIC,
          PRESET_TITLE_PHOTO,
          PRESET_TITLE_LIVE_BURST,
          PRESET_TITLE_BURST,
          PRESET_TITLE_NIGHT,
          PRESET_TITLE_TIME_WARP,
          PRESET_TITLE_TIME_LAPSE,
          PRESET_TITLE_NIGHT_LAPSE,
          PRESET_TITLE_VIDEO,
          PRESET_TITLE_SLOMO,
          PRESET_TITLE_PHOTO_2,
          PRESET_TITLE_PANORAMA,
          PRESET_TITLE_TIME_WARP_2,
          PRESET_TITLE_CUSTOM,
          PRESET_TITLE_AIR,
          PRESET_TITLE_BIKE,
          PRESET_TITLE_EPIC,
          PRESET_TITLE_INDOOR,
          PRESET_TITLE_MOTOR,
          PRESET_TITLE_MOUNTED,
          PRESET_TITLE_OUTDOOR,
          PRESET_TITLE_POV,
          PRESET_TITLE_SELFIE,
          PRESET_TITLE_SKATE,
          PRESET_TITLE_SNOW,
          PRESET_TITLE_TRAIL,
          PRESET_TITLE_TRAVEL,
          PRESET_TITLE_WATER,
          PRESET_TITLE_LOOPING,
          PRESET_TITLE_STARS,
          PRESET_TITLE_ACTION,
          PRESET_TITLE_FOLLOW_CAM,
          PRESET_TITLE_SURF,
          PRESET_TITLE_CITY,
          PRESET_TITLE_SHAKY,
          PRESET_TITLE_CHESTY,
          PRESET_TITLE_HELMET,
          PRESET_TITLE_BITE,
          PRESET_TITLE_CUSTOM_CINEMATIC,
          PRESET_TITLE_VLOG,
          PRESET_TITLE_FPV,
          PRESET_TITLE_HDR,
          PRESET_TITLE_LANDSCAPE,
          PRESET_TITLE_LOG,
          PRESET_TITLE_CUSTOM_SLOMO,
          PRESET_TITLE_TRIPOD,
          PRESET_TITLE_BASIC,
          PRESET_TITLE_ULTRA_SLO_MO,
          PRESET_TITLE_STANDARD_ENDURANCE,
          PRESET_TITLE_ACTIVITY_ENDURANCE,
          PRESET_TITLE_CINEMATIC_ENDURANCE,
          PRESET_TITLE_SLOMO_ENDURANCE,
          PRESET_TITLE_STATIONARY_1,
          PRESET_TITLE_STATIONARY_2,
          PRESET_TITLE_STATIONARY_3,
          PRESET_TITLE_STATIONARY_4,
          PRESET_TITLE_SIMPLE_VIDEO,
          PRESET_TITLE_SIMPLE_TIME_WARP,
          PRESET_TITLE_SIMPLE_SUPER_PHOTO,
          PRESET_TITLE_SIMPLE_NIGHT_PHOTO,
          PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE,
          PRESET_TITLE_HIGHEST_QUALITY,
          PRESET_TITLE_EXTENDED_BATTERY,
          PRESET_TITLE_LONGEST_BATTERY,
          PRESET_TITLE_STAR_TRAIL,
          PRESET_TITLE_LIGHT_PAINTING,
          PRESET_TITLE_LIGHT_TRAIL,
          PRESET_TITLE_FULL_FRAME,
          PRESET_TITLE_STANDARD_QUALITY_VIDEO,
          PRESET_TITLE_BASIC_QUALITY_VIDEO,
          PRESET_TITLE_HIGHEST_QUALITY_VIDEO,
          PRESET_TITLE_USER_DEFINED_CUSTOM_NAME,
          PRESET_TITLE_EASY_STANDARD_PROFILE,
          PRESET_TITLE_EASY_HDR_PROFILE,
          PRESET_TITLE_BURST_SLOMO,
          PRESET_TITLE_4_3_VIDEO,
          PRESET_TITLE_16_9_VIDEO,
          PRESET_TITLE_16_9_SLOMO,
          PRESET_TITLE_TIME_LAPSE_VIDEO,
          PRESET_TITLE_TIME_LAPSE_PHOTO,
          PRESET_TITLE_NIGHT_LAPSE_VIDEO,
          PRESET_TITLE_NIGHT_LAPSE_PHOTO)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPresetTitle =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPresetTitle =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumPresetTitle with name: $name")
  }
}

@pbandk.Export
public data class NotifyPresetStatus(
    val presetGroupArray: List<com.gopro.open_gopro.operations.PresetGroup> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.NotifyPresetStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyPresetStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.NotifyPresetStatus> {
    internal val defaultInstance: com.gopro.open_gopro.operations.NotifyPresetStatus by lazy {
      com.gopro.open_gopro.operations.NotifyPresetStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.NotifyPresetStatus =
        com.gopro.open_gopro.operations.NotifyPresetStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyPresetStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyPresetStatus",
            messageClass = com.gopro.open_gopro.operations.NotifyPresetStatus::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "preset_group_array",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.PresetGroup>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Message(
                                          messageCompanion =
                                              com.gopro.open_gopro.operations.PresetGroup
                                                  .Companion)),
                          jsonName = "presetGroupArray",
                          value =
                              com.gopro.open_gopro.operations.NotifyPresetStatus::presetGroupArray))
                })
  }
}

@pbandk.Export
public data class Preset(
    val id: Int? = null,
    val mode: com.gopro.open_gopro.operations.EnumFlatMode? = null,
    val titleId: com.gopro.open_gopro.operations.EnumPresetTitle? = null,
    val titleNumber: Int? = null,
    val userDefined: Boolean? = null,
    val icon: com.gopro.open_gopro.operations.EnumPresetIcon? = null,
    val settingArray: List<com.gopro.open_gopro.operations.PresetSetting> = emptyList(),
    val isModified: Boolean? = null,
    val isFixed: Boolean? = null,
    val customName: String? = null,
    val isVisible: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.operations.Preset =
      protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.Preset>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.operations.Preset> {
    internal val defaultInstance: com.gopro.open_gopro.operations.Preset by lazy {
      com.gopro.open_gopro.operations.Preset()
    }

    override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.operations.Preset =
        com.gopro.open_gopro.operations.Preset.decodeWithImpl(u)

    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.Preset> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.Preset",
            messageClass = com.gopro.open_gopro.operations.Preset::class,
            messageCompanion = this,
            fields =
                buildList(11) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "id",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "id",
                          value = com.gopro.open_gopro.operations.Preset::id))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "mode",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumFlatMode.Companion,
                                  hasPresence = true),
                          jsonName = "mode",
                          value = com.gopro.open_gopro.operations.Preset::mode))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "title_id",
                          number = 3,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetTitle.Companion,
                                  hasPresence = true),
                          jsonName = "titleId",
                          value = com.gopro.open_gopro.operations.Preset::titleId))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "title_number",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "titleNumber",
                          value = com.gopro.open_gopro.operations.Preset::titleNumber))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "user_defined",
                          number = 5,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "userDefined",
                          value = com.gopro.open_gopro.operations.Preset::userDefined))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "icon",
                          number = 6,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetIcon.Companion,
                                  hasPresence = true),
                          jsonName = "icon",
                          value = com.gopro.open_gopro.operations.Preset::icon))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "setting_array",
                          number = 7,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.PresetSetting>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Message(
                                          messageCompanion =
                                              com.gopro.open_gopro.operations.PresetSetting
                                                  .Companion)),
                          jsonName = "settingArray",
                          value = com.gopro.open_gopro.operations.Preset::settingArray))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "is_modified",
                          number = 8,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "isModified",
                          value = com.gopro.open_gopro.operations.Preset::isModified))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "is_fixed",
                          number = 9,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "isFixed",
                          value = com.gopro.open_gopro.operations.Preset::isFixed))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "custom_name",
                          number = 10,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "customName",
                          value = com.gopro.open_gopro.operations.Preset::customName))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "is_visible",
                          number = 11,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "isVisible",
                          value = com.gopro.open_gopro.operations.Preset::isVisible))
                })
  }
}

@pbandk.Export
internal data class RequestCustomPresetUpdate(
    val titleId: com.gopro.open_gopro.operations.EnumPresetTitle? = null,
    val customName: String? = null,
    val iconId: com.gopro.open_gopro.operations.EnumPresetIcon? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestCustomPresetUpdate = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCustomPresetUpdate>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestCustomPresetUpdate> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.RequestCustomPresetUpdate by lazy {
      com.gopro.open_gopro.operations.RequestCustomPresetUpdate()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestCustomPresetUpdate =
        com.gopro.open_gopro.operations.RequestCustomPresetUpdate.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCustomPresetUpdate> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCustomPresetUpdate",
            messageClass = com.gopro.open_gopro.operations.RequestCustomPresetUpdate::class,
            messageCompanion = this,
            fields =
                buildList(3) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "title_id",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetTitle.Companion,
                                  hasPresence = true),
                          jsonName = "titleId",
                          value =
                              com.gopro.open_gopro.operations.RequestCustomPresetUpdate::titleId))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "custom_name",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "customName",
                          value =
                              com.gopro.open_gopro.operations.RequestCustomPresetUpdate::
                                  customName))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "icon_id",
                          number = 3,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetIcon.Companion,
                                  hasPresence = true),
                          jsonName = "iconId",
                          value =
                              com.gopro.open_gopro.operations.RequestCustomPresetUpdate::iconId))
                })
  }
}

@pbandk.Export
internal data class RequestPresetSetVisibility(
    val id: Int? = null,
    val visible: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestPresetSetVisibility = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestPresetSetVisibility>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestPresetSetVisibility> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.RequestPresetSetVisibility by lazy {
      com.gopro.open_gopro.operations.RequestPresetSetVisibility()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestPresetSetVisibility =
        com.gopro.open_gopro.operations.RequestPresetSetVisibility.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestPresetSetVisibility> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestPresetSetVisibility",
            messageClass = com.gopro.open_gopro.operations.RequestPresetSetVisibility::class,
            messageCompanion = this,
            fields =
                buildList(2) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "id",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "id",
                          value = com.gopro.open_gopro.operations.RequestPresetSetVisibility::id))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "visible",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "visible",
                          value =
                              com.gopro.open_gopro.operations.RequestPresetSetVisibility::visible))
                })
  }
}

@pbandk.Export
public data class PresetGroup(
    val id: com.gopro.open_gopro.operations.EnumPresetGroup? = null,
    val presetArray: List<com.gopro.open_gopro.operations.Preset> = emptyList(),
    val canAddPreset: Boolean? = null,
    val icon: com.gopro.open_gopro.operations.EnumPresetGroupIcon? = null,
    val modeArray: List<com.gopro.open_gopro.operations.EnumFlatMode> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.operations.PresetGroup =
      protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetGroup>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.PresetGroup> {
    internal val defaultInstance: com.gopro.open_gopro.operations.PresetGroup by lazy {
      com.gopro.open_gopro.operations.PresetGroup()
    }

    override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.operations.PresetGroup =
        com.gopro.open_gopro.operations.PresetGroup.decodeWithImpl(u)

    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetGroup> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.PresetGroup",
            messageClass = com.gopro.open_gopro.operations.PresetGroup::class,
            messageCompanion = this,
            fields =
                buildList(5) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "id",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetGroup.Companion,
                                  hasPresence = true),
                          jsonName = "id",
                          value = com.gopro.open_gopro.operations.PresetGroup::id))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "preset_array",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.Preset>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Message(
                                          messageCompanion =
                                              com.gopro.open_gopro.operations.Preset.Companion)),
                          jsonName = "presetArray",
                          value = com.gopro.open_gopro.operations.PresetGroup::presetArray))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "can_add_preset",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "canAddPreset",
                          value = com.gopro.open_gopro.operations.PresetGroup::canAddPreset))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "icon",
                          number = 4,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumPresetGroupIcon.Companion,
                                  hasPresence = true),
                          jsonName = "icon",
                          value = com.gopro.open_gopro.operations.PresetGroup::icon))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "mode_array",
                          number = 5,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumFlatMode>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations.EnumFlatMode
                                                  .Companion)),
                          jsonName = "modeArray",
                          value = com.gopro.open_gopro.operations.PresetGroup::modeArray))
                })
  }
}

@pbandk.Export
public data class PresetSetting(
    val id: Int? = null,
    val value: Int? = null,
    val isCaption: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.PresetSetting = protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetSetting>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.PresetSetting> {
    internal val defaultInstance: com.gopro.open_gopro.operations.PresetSetting by lazy {
      com.gopro.open_gopro.operations.PresetSetting()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.PresetSetting =
        com.gopro.open_gopro.operations.PresetSetting.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetSetting> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.PresetSetting",
            messageClass = com.gopro.open_gopro.operations.PresetSetting::class,
            messageCompanion = this,
            fields =
                buildList(3) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "id",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "id",
                          value = com.gopro.open_gopro.operations.PresetSetting::id))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "value",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "value",
                          value = com.gopro.open_gopro.operations.PresetSetting::value))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "is_caption",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "isCaption",
                          value = com.gopro.open_gopro.operations.PresetSetting::isCaption))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyPresetStatus")
internal fun NotifyPresetStatus?.orDefault(): com.gopro.open_gopro.operations.NotifyPresetStatus =
    this ?: NotifyPresetStatus.defaultInstance

private fun NotifyPresetStatus.protoMergeImpl(plus: pbandk.Message?): NotifyPresetStatus =
    (plus as? NotifyPresetStatus)?.let {
      it.copy(
          presetGroupArray = presetGroupArray + plus.presetGroupArray,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyPresetStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): NotifyPresetStatus {
  var presetGroupArray: pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.PresetGroup>? =
      null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 ->
              presetGroupArray =
                  (presetGroupArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<com.gopro.open_gopro.operations.PresetGroup>
                  }
        }
      }

  return NotifyPresetStatus(pbandk.ListWithSize.Builder.fixed(presetGroupArray), unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPreset")
internal fun Preset?.orDefault(): com.gopro.open_gopro.operations.Preset =
    this ?: Preset.defaultInstance

private fun Preset.protoMergeImpl(plus: pbandk.Message?): Preset =
    (plus as? Preset)?.let {
      it.copy(
          id = plus.id ?: id,
          mode = plus.mode ?: mode,
          titleId = plus.titleId ?: titleId,
          titleNumber = plus.titleNumber ?: titleNumber,
          userDefined = plus.userDefined ?: userDefined,
          icon = plus.icon ?: icon,
          settingArray = settingArray + plus.settingArray,
          isModified = plus.isModified ?: isModified,
          isFixed = plus.isFixed ?: isFixed,
          customName = plus.customName ?: customName,
          isVisible = plus.isVisible ?: isVisible,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun Preset.Companion.decodeWithImpl(u: pbandk.MessageDecoder): Preset {
  var id: Int? = null
  var mode: com.gopro.open_gopro.operations.EnumFlatMode? = null
  var titleId: com.gopro.open_gopro.operations.EnumPresetTitle? = null
  var titleNumber: Int? = null
  var userDefined: Boolean? = null
  var icon: com.gopro.open_gopro.operations.EnumPresetIcon? = null
  var settingArray: pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.PresetSetting>? =
      null
  var isModified: Boolean? = null
  var isFixed: Boolean? = null
  var customName: String? = null
  var isVisible: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> id = _fieldValue as Int
          2 -> mode = _fieldValue as com.gopro.open_gopro.operations.EnumFlatMode
          3 -> titleId = _fieldValue as com.gopro.open_gopro.operations.EnumPresetTitle
          4 -> titleNumber = _fieldValue as Int
          5 -> userDefined = _fieldValue as Boolean
          6 -> icon = _fieldValue as com.gopro.open_gopro.operations.EnumPresetIcon
          7 ->
              settingArray =
                  (settingArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<com.gopro.open_gopro.operations.PresetSetting>
                  }
          8 -> isModified = _fieldValue as Boolean
          9 -> isFixed = _fieldValue as Boolean
          10 -> customName = _fieldValue as String
          11 -> isVisible = _fieldValue as Boolean
        }
      }

  return Preset(
      id,
      mode,
      titleId,
      titleNumber,
      userDefined,
      icon,
      pbandk.ListWithSize.Builder.fixed(settingArray),
      isModified,
      isFixed,
      customName,
      isVisible,
      unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCustomPresetUpdate")
internal fun RequestCustomPresetUpdate?.orDefault():
    com.gopro.open_gopro.operations.RequestCustomPresetUpdate =
    this ?: RequestCustomPresetUpdate.defaultInstance

private fun RequestCustomPresetUpdate.protoMergeImpl(
    plus: pbandk.Message?
): RequestCustomPresetUpdate =
    (plus as? RequestCustomPresetUpdate)?.let {
      it.copy(
          titleId = plus.titleId ?: titleId,
          customName = plus.customName ?: customName,
          iconId = plus.iconId ?: iconId,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCustomPresetUpdate.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestCustomPresetUpdate {
  var titleId: com.gopro.open_gopro.operations.EnumPresetTitle? = null
  var customName: String? = null
  var iconId: com.gopro.open_gopro.operations.EnumPresetIcon? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> titleId = _fieldValue as com.gopro.open_gopro.operations.EnumPresetTitle
          2 -> customName = _fieldValue as String
          3 -> iconId = _fieldValue as com.gopro.open_gopro.operations.EnumPresetIcon
        }
      }

  return RequestCustomPresetUpdate(titleId, customName, iconId, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestPresetSetVisibility")
internal fun RequestPresetSetVisibility?.orDefault():
    com.gopro.open_gopro.operations.RequestPresetSetVisibility =
    this ?: RequestPresetSetVisibility.defaultInstance

private fun RequestPresetSetVisibility.protoMergeImpl(
    plus: pbandk.Message?
): RequestPresetSetVisibility =
    (plus as? RequestPresetSetVisibility)?.let {
      it.copy(
          id = plus.id ?: id,
          visible = plus.visible ?: visible,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestPresetSetVisibility.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestPresetSetVisibility {
  var id: Int? = null
  var visible: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> id = _fieldValue as Int
          2 -> visible = _fieldValue as Boolean
        }
      }

  return RequestPresetSetVisibility(id, visible, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPresetGroup")
internal fun PresetGroup?.orDefault(): com.gopro.open_gopro.operations.PresetGroup =
    this ?: PresetGroup.defaultInstance

private fun PresetGroup.protoMergeImpl(plus: pbandk.Message?): PresetGroup =
    (plus as? PresetGroup)?.let {
      it.copy(
          id = plus.id ?: id,
          presetArray = presetArray + plus.presetArray,
          canAddPreset = plus.canAddPreset ?: canAddPreset,
          icon = plus.icon ?: icon,
          modeArray = modeArray + plus.modeArray,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun PresetGroup.Companion.decodeWithImpl(u: pbandk.MessageDecoder): PresetGroup {
  var id: com.gopro.open_gopro.operations.EnumPresetGroup? = null
  var presetArray: pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.Preset>? = null
  var canAddPreset: Boolean? = null
  var icon: com.gopro.open_gopro.operations.EnumPresetGroupIcon? = null
  var modeArray: pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumFlatMode>? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> id = _fieldValue as com.gopro.open_gopro.operations.EnumPresetGroup
          2 ->
              presetArray =
                  (presetArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as kotlin.sequences.Sequence<com.gopro.open_gopro.operations.Preset>
                  }
          3 -> canAddPreset = _fieldValue as Boolean
          4 -> icon = _fieldValue as com.gopro.open_gopro.operations.EnumPresetGroupIcon
          5 ->
              modeArray =
                  (modeArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<com.gopro.open_gopro.operations.EnumFlatMode>
                  }
        }
      }

  return PresetGroup(
      id,
      pbandk.ListWithSize.Builder.fixed(presetArray),
      canAddPreset,
      icon,
      pbandk.ListWithSize.Builder.fixed(modeArray),
      unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPresetSetting")
internal fun PresetSetting?.orDefault(): com.gopro.open_gopro.operations.PresetSetting =
    this ?: PresetSetting.defaultInstance

private fun PresetSetting.protoMergeImpl(plus: pbandk.Message?): PresetSetting =
    (plus as? PresetSetting)?.let {
      it.copy(
          id = plus.id ?: id,
          value = plus.value ?: value,
          isCaption = plus.isCaption ?: isCaption,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun PresetSetting.Companion.decodeWithImpl(u: pbandk.MessageDecoder): PresetSetting {
  var id: Int? = null
  var value: Int? = null
  var isCaption: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> id = _fieldValue as Int
          2 -> value = _fieldValue as Int
          3 -> isCaption = _fieldValue as Boolean
        }
      }

  return PresetSetting(id, value, isCaption, unknownFields)
}
