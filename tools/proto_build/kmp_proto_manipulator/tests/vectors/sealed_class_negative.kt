/* sealed_class_negative.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025 */

@pbandk.Export
internal sealed class NotReal(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is com.gopro.open_gopro.operations.EnumPresetGroup && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumPresetGroup.${name ?: "UNRECOGNIZED"}(value=$value)"
    internal object PRESET_GROUP_ID_VIDEO : EnumPresetGroup(1000, "PRESET_GROUP_ID_VIDEO")
    internal object PRESET_GROUP_ID_PHOTO : EnumPresetGroup(1001, "PRESET_GROUP_ID_PHOTO")
    internal object PRESET_GROUP_ID_TIMELAPSE : EnumPresetGroup(1002, "PRESET_GROUP_ID_TIMELAPSE")
    internal class UNRECOGNIZED(value: Int) : EnumPresetGroup(value)
    internal companion object : pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPresetGroup> {
        internal val values: List<com.gopro.open_gopro.operations.EnumPresetGroup> by lazy { listOf(PRESET_GROUP_ID_VIDEO, PRESET_GROUP_ID_PHOTO, PRESET_GROUP_ID_TIMELAPSE) }
        override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPresetGroup = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPresetGroup = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumPresetGroup with name: $name")
    }
}