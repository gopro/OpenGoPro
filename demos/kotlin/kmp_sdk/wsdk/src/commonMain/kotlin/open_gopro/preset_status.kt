@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumFlatMode(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumFlatMode && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumFlatMode.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object FLAT_MODE_UNKNOWN : EnumFlatMode(-1, "FLAT_MODE_UNKNOWN")
    public object FLAT_MODE_PLAYBACK : EnumFlatMode(4, "FLAT_MODE_PLAYBACK")
    public object FLAT_MODE_SETUP : EnumFlatMode(5, "FLAT_MODE_SETUP")
    public object FLAT_MODE_VIDEO : EnumFlatMode(12, "FLAT_MODE_VIDEO")
    public object FLAT_MODE_TIME_LAPSE_VIDEO : EnumFlatMode(13, "FLAT_MODE_TIME_LAPSE_VIDEO")
    public object FLAT_MODE_LOOPING : EnumFlatMode(15, "FLAT_MODE_LOOPING")
    public object FLAT_MODE_PHOTO_SINGLE : EnumFlatMode(16, "FLAT_MODE_PHOTO_SINGLE")
    public object FLAT_MODE_PHOTO : EnumFlatMode(17, "FLAT_MODE_PHOTO")
    public object FLAT_MODE_PHOTO_NIGHT : EnumFlatMode(18, "FLAT_MODE_PHOTO_NIGHT")
    public object FLAT_MODE_PHOTO_BURST : EnumFlatMode(19, "FLAT_MODE_PHOTO_BURST")
    public object FLAT_MODE_TIME_LAPSE_PHOTO : EnumFlatMode(20, "FLAT_MODE_TIME_LAPSE_PHOTO")
    public object FLAT_MODE_NIGHT_LAPSE_PHOTO : EnumFlatMode(21, "FLAT_MODE_NIGHT_LAPSE_PHOTO")
    public object FLAT_MODE_BROADCAST_RECORD : EnumFlatMode(22, "FLAT_MODE_BROADCAST_RECORD")
    public object FLAT_MODE_BROADCAST_BROADCAST : EnumFlatMode(23, "FLAT_MODE_BROADCAST_BROADCAST")
    public object FLAT_MODE_TIME_WARP_VIDEO : EnumFlatMode(24, "FLAT_MODE_TIME_WARP_VIDEO")
    public object FLAT_MODE_LIVE_BURST : EnumFlatMode(25, "FLAT_MODE_LIVE_BURST")
    public object FLAT_MODE_NIGHT_LAPSE_VIDEO : EnumFlatMode(26, "FLAT_MODE_NIGHT_LAPSE_VIDEO")
    public object FLAT_MODE_SLOMO : EnumFlatMode(27, "FLAT_MODE_SLOMO")
    public object FLAT_MODE_IDLE : EnumFlatMode(28, "FLAT_MODE_IDLE")
    public object FLAT_MODE_VIDEO_STAR_TRAIL : EnumFlatMode(29, "FLAT_MODE_VIDEO_STAR_TRAIL")
    public object FLAT_MODE_VIDEO_LIGHT_PAINTING : EnumFlatMode(30, "FLAT_MODE_VIDEO_LIGHT_PAINTING")
    public object FLAT_MODE_VIDEO_LIGHT_TRAIL : EnumFlatMode(31, "FLAT_MODE_VIDEO_LIGHT_TRAIL")
    public object FLAT_MODE_VIDEO_BURST_SLOMO : EnumFlatMode(32, "FLAT_MODE_VIDEO_BURST_SLOMO")
    public class UNRECOGNIZED(value: Int) : EnumFlatMode(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumFlatMode> {
        public val values: List<open_gopro.EnumFlatMode> by lazy { listOf(FLAT_MODE_UNKNOWN, FLAT_MODE_PLAYBACK, FLAT_MODE_SETUP, FLAT_MODE_VIDEO, FLAT_MODE_TIME_LAPSE_VIDEO, FLAT_MODE_LOOPING, FLAT_MODE_PHOTO_SINGLE, FLAT_MODE_PHOTO, FLAT_MODE_PHOTO_NIGHT, FLAT_MODE_PHOTO_BURST, FLAT_MODE_TIME_LAPSE_PHOTO, FLAT_MODE_NIGHT_LAPSE_PHOTO, FLAT_MODE_BROADCAST_RECORD, FLAT_MODE_BROADCAST_BROADCAST, FLAT_MODE_TIME_WARP_VIDEO, FLAT_MODE_LIVE_BURST, FLAT_MODE_NIGHT_LAPSE_VIDEO, FLAT_MODE_SLOMO, FLAT_MODE_IDLE, FLAT_MODE_VIDEO_STAR_TRAIL, FLAT_MODE_VIDEO_LIGHT_PAINTING, FLAT_MODE_VIDEO_LIGHT_TRAIL, FLAT_MODE_VIDEO_BURST_SLOMO) }
        override fun fromValue(value: Int): open_gopro.EnumFlatMode = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumFlatMode = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumFlatMode with name: $name")
    }
}

@pbandk.Export
public sealed class EnumPresetGroup(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumPresetGroup && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumPresetGroup.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object PRESET_GROUP_ID_VIDEO : EnumPresetGroup(1000, "PRESET_GROUP_ID_VIDEO")
    public object PRESET_GROUP_ID_PHOTO : EnumPresetGroup(1001, "PRESET_GROUP_ID_PHOTO")
    public object PRESET_GROUP_ID_TIMELAPSE : EnumPresetGroup(1002, "PRESET_GROUP_ID_TIMELAPSE")
    public class UNRECOGNIZED(value: Int) : EnumPresetGroup(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumPresetGroup> {
        public val values: List<open_gopro.EnumPresetGroup> by lazy { listOf(PRESET_GROUP_ID_VIDEO, PRESET_GROUP_ID_PHOTO, PRESET_GROUP_ID_TIMELAPSE) }
        override fun fromValue(value: Int): open_gopro.EnumPresetGroup = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumPresetGroup = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumPresetGroup with name: $name")
    }
}

@pbandk.Export
public sealed class EnumPresetGroupIcon(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumPresetGroupIcon && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumPresetGroupIcon.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object PRESET_GROUP_VIDEO_ICON_ID : EnumPresetGroupIcon(0, "PRESET_GROUP_VIDEO_ICON_ID")
    public object PRESET_GROUP_PHOTO_ICON_ID : EnumPresetGroupIcon(1, "PRESET_GROUP_PHOTO_ICON_ID")
    public object PRESET_GROUP_TIMELAPSE_ICON_ID : EnumPresetGroupIcon(2, "PRESET_GROUP_TIMELAPSE_ICON_ID")
    public object PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID : EnumPresetGroupIcon(3, "PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID")
    public object PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID : EnumPresetGroupIcon(4, "PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID")
    public object PRESET_GROUP_MAX_VIDEO_ICON_ID : EnumPresetGroupIcon(5, "PRESET_GROUP_MAX_VIDEO_ICON_ID")
    public object PRESET_GROUP_MAX_PHOTO_ICON_ID : EnumPresetGroupIcon(6, "PRESET_GROUP_MAX_PHOTO_ICON_ID")
    public object PRESET_GROUP_MAX_TIMELAPSE_ICON_ID : EnumPresetGroupIcon(7, "PRESET_GROUP_MAX_TIMELAPSE_ICON_ID")
    public object PRESET_GROUP_ND_MOD_VIDEO_ICON_ID : EnumPresetGroupIcon(8, "PRESET_GROUP_ND_MOD_VIDEO_ICON_ID")
    public object PRESET_GROUP_ND_MOD_PHOTO_ICON_ID : EnumPresetGroupIcon(9, "PRESET_GROUP_ND_MOD_PHOTO_ICON_ID")
    public object PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID : EnumPresetGroupIcon(10, "PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID")
    public class UNRECOGNIZED(value: Int) : EnumPresetGroupIcon(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumPresetGroupIcon> {
        public val values: List<open_gopro.EnumPresetGroupIcon> by lazy { listOf(PRESET_GROUP_VIDEO_ICON_ID, PRESET_GROUP_PHOTO_ICON_ID, PRESET_GROUP_TIMELAPSE_ICON_ID, PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID, PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID, PRESET_GROUP_MAX_VIDEO_ICON_ID, PRESET_GROUP_MAX_PHOTO_ICON_ID, PRESET_GROUP_MAX_TIMELAPSE_ICON_ID, PRESET_GROUP_ND_MOD_VIDEO_ICON_ID, PRESET_GROUP_ND_MOD_PHOTO_ICON_ID, PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID) }
        override fun fromValue(value: Int): open_gopro.EnumPresetGroupIcon = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumPresetGroupIcon = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumPresetGroupIcon with name: $name")
    }
}

@pbandk.Export
public sealed class EnumPresetIcon(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumPresetIcon && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumPresetIcon.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object PRESET_ICON_VIDEO : EnumPresetIcon(0, "PRESET_ICON_VIDEO")
    public object PRESET_ICON_ACTIVITY : EnumPresetIcon(1, "PRESET_ICON_ACTIVITY")
    public object PRESET_ICON_CINEMATIC : EnumPresetIcon(2, "PRESET_ICON_CINEMATIC")
    public object PRESET_ICON_PHOTO : EnumPresetIcon(3, "PRESET_ICON_PHOTO")
    public object PRESET_ICON_LIVE_BURST : EnumPresetIcon(4, "PRESET_ICON_LIVE_BURST")
    public object PRESET_ICON_BURST : EnumPresetIcon(5, "PRESET_ICON_BURST")
    public object PRESET_ICON_PHOTO_NIGHT : EnumPresetIcon(6, "PRESET_ICON_PHOTO_NIGHT")
    public object PRESET_ICON_TIMEWARP : EnumPresetIcon(7, "PRESET_ICON_TIMEWARP")
    public object PRESET_ICON_TIMELAPSE : EnumPresetIcon(8, "PRESET_ICON_TIMELAPSE")
    public object PRESET_ICON_NIGHTLAPSE : EnumPresetIcon(9, "PRESET_ICON_NIGHTLAPSE")
    public object PRESET_ICON_SNAIL : EnumPresetIcon(10, "PRESET_ICON_SNAIL")
    public object PRESET_ICON_VIDEO_2 : EnumPresetIcon(11, "PRESET_ICON_VIDEO_2")
    public object PRESET_ICON_PHOTO_2 : EnumPresetIcon(13, "PRESET_ICON_PHOTO_2")
    public object PRESET_ICON_PANORAMA : EnumPresetIcon(14, "PRESET_ICON_PANORAMA")
    public object PRESET_ICON_BURST_2 : EnumPresetIcon(15, "PRESET_ICON_BURST_2")
    public object PRESET_ICON_TIMEWARP_2 : EnumPresetIcon(16, "PRESET_ICON_TIMEWARP_2")
    public object PRESET_ICON_TIMELAPSE_2 : EnumPresetIcon(17, "PRESET_ICON_TIMELAPSE_2")
    public object PRESET_ICON_CUSTOM : EnumPresetIcon(18, "PRESET_ICON_CUSTOM")
    public object PRESET_ICON_AIR : EnumPresetIcon(19, "PRESET_ICON_AIR")
    public object PRESET_ICON_BIKE : EnumPresetIcon(20, "PRESET_ICON_BIKE")
    public object PRESET_ICON_EPIC : EnumPresetIcon(21, "PRESET_ICON_EPIC")
    public object PRESET_ICON_INDOOR : EnumPresetIcon(22, "PRESET_ICON_INDOOR")
    public object PRESET_ICON_MOTOR : EnumPresetIcon(23, "PRESET_ICON_MOTOR")
    public object PRESET_ICON_MOUNTED : EnumPresetIcon(24, "PRESET_ICON_MOUNTED")
    public object PRESET_ICON_OUTDOOR : EnumPresetIcon(25, "PRESET_ICON_OUTDOOR")
    public object PRESET_ICON_POV : EnumPresetIcon(26, "PRESET_ICON_POV")
    public object PRESET_ICON_SELFIE : EnumPresetIcon(27, "PRESET_ICON_SELFIE")
    public object PRESET_ICON_SKATE : EnumPresetIcon(28, "PRESET_ICON_SKATE")
    public object PRESET_ICON_SNOW : EnumPresetIcon(29, "PRESET_ICON_SNOW")
    public object PRESET_ICON_TRAIL : EnumPresetIcon(30, "PRESET_ICON_TRAIL")
    public object PRESET_ICON_TRAVEL : EnumPresetIcon(31, "PRESET_ICON_TRAVEL")
    public object PRESET_ICON_WATER : EnumPresetIcon(32, "PRESET_ICON_WATER")
    public object PRESET_ICON_LOOPING : EnumPresetIcon(33, "PRESET_ICON_LOOPING")
    public object PRESET_ICON_STARS : EnumPresetIcon(34, "PRESET_ICON_STARS")
    public object PRESET_ICON_ACTION : EnumPresetIcon(35, "PRESET_ICON_ACTION")
    public object PRESET_ICON_FOLLOW_CAM : EnumPresetIcon(36, "PRESET_ICON_FOLLOW_CAM")
    public object PRESET_ICON_SURF : EnumPresetIcon(37, "PRESET_ICON_SURF")
    public object PRESET_ICON_CITY : EnumPresetIcon(38, "PRESET_ICON_CITY")
    public object PRESET_ICON_SHAKY : EnumPresetIcon(39, "PRESET_ICON_SHAKY")
    public object PRESET_ICON_CHESTY : EnumPresetIcon(40, "PRESET_ICON_CHESTY")
    public object PRESET_ICON_HELMET : EnumPresetIcon(41, "PRESET_ICON_HELMET")
    public object PRESET_ICON_BITE : EnumPresetIcon(42, "PRESET_ICON_BITE")
    public object PRESET_ICON_CUSTOM_CINEMATIC : EnumPresetIcon(43, "PRESET_ICON_CUSTOM_CINEMATIC")
    public object PRESET_ICON_VLOG : EnumPresetIcon(44, "PRESET_ICON_VLOG")
    public object PRESET_ICON_FPV : EnumPresetIcon(45, "PRESET_ICON_FPV")
    public object PRESET_ICON_HDR : EnumPresetIcon(46, "PRESET_ICON_HDR")
    public object PRESET_ICON_LANDSCAPE : EnumPresetIcon(47, "PRESET_ICON_LANDSCAPE")
    public object PRESET_ICON_LOG : EnumPresetIcon(48, "PRESET_ICON_LOG")
    public object PRESET_ICON_CUSTOM_SLOMO : EnumPresetIcon(49, "PRESET_ICON_CUSTOM_SLOMO")
    public object PRESET_ICON_TRIPOD : EnumPresetIcon(50, "PRESET_ICON_TRIPOD")
    public object PRESET_ICON_MAX_VIDEO : EnumPresetIcon(55, "PRESET_ICON_MAX_VIDEO")
    public object PRESET_ICON_MAX_PHOTO : EnumPresetIcon(56, "PRESET_ICON_MAX_PHOTO")
    public object PRESET_ICON_MAX_TIMEWARP : EnumPresetIcon(57, "PRESET_ICON_MAX_TIMEWARP")
    public object PRESET_ICON_BASIC : EnumPresetIcon(58, "PRESET_ICON_BASIC")
    public object PRESET_ICON_ULTRA_SLO_MO : EnumPresetIcon(59, "PRESET_ICON_ULTRA_SLO_MO")
    public object PRESET_ICON_STANDARD_ENDURANCE : EnumPresetIcon(60, "PRESET_ICON_STANDARD_ENDURANCE")
    public object PRESET_ICON_ACTIVITY_ENDURANCE : EnumPresetIcon(61, "PRESET_ICON_ACTIVITY_ENDURANCE")
    public object PRESET_ICON_CINEMATIC_ENDURANCE : EnumPresetIcon(62, "PRESET_ICON_CINEMATIC_ENDURANCE")
    public object PRESET_ICON_SLOMO_ENDURANCE : EnumPresetIcon(63, "PRESET_ICON_SLOMO_ENDURANCE")
    public object PRESET_ICON_STATIONARY_1 : EnumPresetIcon(64, "PRESET_ICON_STATIONARY_1")
    public object PRESET_ICON_STATIONARY_2 : EnumPresetIcon(65, "PRESET_ICON_STATIONARY_2")
    public object PRESET_ICON_STATIONARY_3 : EnumPresetIcon(66, "PRESET_ICON_STATIONARY_3")
    public object PRESET_ICON_STATIONARY_4 : EnumPresetIcon(67, "PRESET_ICON_STATIONARY_4")
    public object PRESET_ICON_SIMPLE_SUPER_PHOTO : EnumPresetIcon(70, "PRESET_ICON_SIMPLE_SUPER_PHOTO")
    public object PRESET_ICON_SIMPLE_NIGHT_PHOTO : EnumPresetIcon(71, "PRESET_ICON_SIMPLE_NIGHT_PHOTO")
    public object PRESET_ICON_HIGHEST_QUALITY_VIDEO : EnumPresetIcon(73, "PRESET_ICON_HIGHEST_QUALITY_VIDEO")
    public object PRESET_ICON_STANDARD_QUALITY_VIDEO : EnumPresetIcon(74, "PRESET_ICON_STANDARD_QUALITY_VIDEO")
    public object PRESET_ICON_BASIC_QUALITY_VIDEO : EnumPresetIcon(75, "PRESET_ICON_BASIC_QUALITY_VIDEO")
    public object PRESET_ICON_STAR_TRAIL : EnumPresetIcon(76, "PRESET_ICON_STAR_TRAIL")
    public object PRESET_ICON_LIGHT_PAINTING : EnumPresetIcon(77, "PRESET_ICON_LIGHT_PAINTING")
    public object PRESET_ICON_LIGHT_TRAIL : EnumPresetIcon(78, "PRESET_ICON_LIGHT_TRAIL")
    public object PRESET_ICON_FULL_FRAME : EnumPresetIcon(79, "PRESET_ICON_FULL_FRAME")
    public object PRESET_ICON_EASY_MAX_VIDEO : EnumPresetIcon(80, "PRESET_ICON_EASY_MAX_VIDEO")
    public object PRESET_ICON_EASY_MAX_PHOTO : EnumPresetIcon(81, "PRESET_ICON_EASY_MAX_PHOTO")
    public object PRESET_ICON_EASY_MAX_TIMEWARP : EnumPresetIcon(82, "PRESET_ICON_EASY_MAX_TIMEWARP")
    public object PRESET_ICON_EASY_MAX_STAR_TRAIL : EnumPresetIcon(83, "PRESET_ICON_EASY_MAX_STAR_TRAIL")
    public object PRESET_ICON_EASY_MAX_LIGHT_PAINTING : EnumPresetIcon(84, "PRESET_ICON_EASY_MAX_LIGHT_PAINTING")
    public object PRESET_ICON_EASY_MAX_LIGHT_TRAIL : EnumPresetIcon(85, "PRESET_ICON_EASY_MAX_LIGHT_TRAIL")
    public object PRESET_ICON_MAX_STAR_TRAIL : EnumPresetIcon(89, "PRESET_ICON_MAX_STAR_TRAIL")
    public object PRESET_ICON_MAX_LIGHT_PAINTING : EnumPresetIcon(90, "PRESET_ICON_MAX_LIGHT_PAINTING")
    public object PRESET_ICON_MAX_LIGHT_TRAIL : EnumPresetIcon(91, "PRESET_ICON_MAX_LIGHT_TRAIL")
    public object PRESET_ICON_EASY_STANDARD_PROFILE : EnumPresetIcon(100, "PRESET_ICON_EASY_STANDARD_PROFILE")
    public object PRESET_ICON_EASY_HDR_PROFILE : EnumPresetIcon(101, "PRESET_ICON_EASY_HDR_PROFILE")
    public object PRESET_ICON_BURST_SLOMO : EnumPresetIcon(102, "PRESET_ICON_BURST_SLOMO")
    public object PRESET_ICON_TIMELAPSE_PHOTO : EnumPresetIcon(1000, "PRESET_ICON_TIMELAPSE_PHOTO")
    public object PRESET_ICON_NIGHTLAPSE_PHOTO : EnumPresetIcon(1001, "PRESET_ICON_NIGHTLAPSE_PHOTO")
    public class UNRECOGNIZED(value: Int) : EnumPresetIcon(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumPresetIcon> {
        public val values: List<open_gopro.EnumPresetIcon> by lazy { listOf(PRESET_ICON_VIDEO, PRESET_ICON_ACTIVITY, PRESET_ICON_CINEMATIC, PRESET_ICON_PHOTO, PRESET_ICON_LIVE_BURST, PRESET_ICON_BURST, PRESET_ICON_PHOTO_NIGHT, PRESET_ICON_TIMEWARP, PRESET_ICON_TIMELAPSE, PRESET_ICON_NIGHTLAPSE, PRESET_ICON_SNAIL, PRESET_ICON_VIDEO_2, PRESET_ICON_PHOTO_2, PRESET_ICON_PANORAMA, PRESET_ICON_BURST_2, PRESET_ICON_TIMEWARP_2, PRESET_ICON_TIMELAPSE_2, PRESET_ICON_CUSTOM, PRESET_ICON_AIR, PRESET_ICON_BIKE, PRESET_ICON_EPIC, PRESET_ICON_INDOOR, PRESET_ICON_MOTOR, PRESET_ICON_MOUNTED, PRESET_ICON_OUTDOOR, PRESET_ICON_POV, PRESET_ICON_SELFIE, PRESET_ICON_SKATE, PRESET_ICON_SNOW, PRESET_ICON_TRAIL, PRESET_ICON_TRAVEL, PRESET_ICON_WATER, PRESET_ICON_LOOPING, PRESET_ICON_STARS, PRESET_ICON_ACTION, PRESET_ICON_FOLLOW_CAM, PRESET_ICON_SURF, PRESET_ICON_CITY, PRESET_ICON_SHAKY, PRESET_ICON_CHESTY, PRESET_ICON_HELMET, PRESET_ICON_BITE, PRESET_ICON_CUSTOM_CINEMATIC, PRESET_ICON_VLOG, PRESET_ICON_FPV, PRESET_ICON_HDR, PRESET_ICON_LANDSCAPE, PRESET_ICON_LOG, PRESET_ICON_CUSTOM_SLOMO, PRESET_ICON_TRIPOD, PRESET_ICON_MAX_VIDEO, PRESET_ICON_MAX_PHOTO, PRESET_ICON_MAX_TIMEWARP, PRESET_ICON_BASIC, PRESET_ICON_ULTRA_SLO_MO, PRESET_ICON_STANDARD_ENDURANCE, PRESET_ICON_ACTIVITY_ENDURANCE, PRESET_ICON_CINEMATIC_ENDURANCE, PRESET_ICON_SLOMO_ENDURANCE, PRESET_ICON_STATIONARY_1, PRESET_ICON_STATIONARY_2, PRESET_ICON_STATIONARY_3, PRESET_ICON_STATIONARY_4, PRESET_ICON_SIMPLE_SUPER_PHOTO, PRESET_ICON_SIMPLE_NIGHT_PHOTO, PRESET_ICON_HIGHEST_QUALITY_VIDEO, PRESET_ICON_STANDARD_QUALITY_VIDEO, PRESET_ICON_BASIC_QUALITY_VIDEO, PRESET_ICON_STAR_TRAIL, PRESET_ICON_LIGHT_PAINTING, PRESET_ICON_LIGHT_TRAIL, PRESET_ICON_FULL_FRAME, PRESET_ICON_EASY_MAX_VIDEO, PRESET_ICON_EASY_MAX_PHOTO, PRESET_ICON_EASY_MAX_TIMEWARP, PRESET_ICON_EASY_MAX_STAR_TRAIL, PRESET_ICON_EASY_MAX_LIGHT_PAINTING, PRESET_ICON_EASY_MAX_LIGHT_TRAIL, PRESET_ICON_MAX_STAR_TRAIL, PRESET_ICON_MAX_LIGHT_PAINTING, PRESET_ICON_MAX_LIGHT_TRAIL, PRESET_ICON_EASY_STANDARD_PROFILE, PRESET_ICON_EASY_HDR_PROFILE, PRESET_ICON_BURST_SLOMO, PRESET_ICON_TIMELAPSE_PHOTO, PRESET_ICON_NIGHTLAPSE_PHOTO) }
        override fun fromValue(value: Int): open_gopro.EnumPresetIcon = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumPresetIcon = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumPresetIcon with name: $name")
    }
}

@pbandk.Export
public sealed class EnumPresetTitle(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumPresetTitle && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumPresetTitle.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object PRESET_TITLE_ACTIVITY : EnumPresetTitle(0, "PRESET_TITLE_ACTIVITY")
    public object PRESET_TITLE_STANDARD : EnumPresetTitle(1, "PRESET_TITLE_STANDARD")
    public object PRESET_TITLE_CINEMATIC : EnumPresetTitle(2, "PRESET_TITLE_CINEMATIC")
    public object PRESET_TITLE_PHOTO : EnumPresetTitle(3, "PRESET_TITLE_PHOTO")
    public object PRESET_TITLE_LIVE_BURST : EnumPresetTitle(4, "PRESET_TITLE_LIVE_BURST")
    public object PRESET_TITLE_BURST : EnumPresetTitle(5, "PRESET_TITLE_BURST")
    public object PRESET_TITLE_NIGHT : EnumPresetTitle(6, "PRESET_TITLE_NIGHT")
    public object PRESET_TITLE_TIME_WARP : EnumPresetTitle(7, "PRESET_TITLE_TIME_WARP")
    public object PRESET_TITLE_TIME_LAPSE : EnumPresetTitle(8, "PRESET_TITLE_TIME_LAPSE")
    public object PRESET_TITLE_NIGHT_LAPSE : EnumPresetTitle(9, "PRESET_TITLE_NIGHT_LAPSE")
    public object PRESET_TITLE_VIDEO : EnumPresetTitle(10, "PRESET_TITLE_VIDEO")
    public object PRESET_TITLE_SLOMO : EnumPresetTitle(11, "PRESET_TITLE_SLOMO")
    public object PRESET_TITLE_PHOTO_2 : EnumPresetTitle(13, "PRESET_TITLE_PHOTO_2")
    public object PRESET_TITLE_PANORAMA : EnumPresetTitle(14, "PRESET_TITLE_PANORAMA")
    public object PRESET_TITLE_TIME_WARP_2 : EnumPresetTitle(16, "PRESET_TITLE_TIME_WARP_2")
    public object PRESET_TITLE_CUSTOM : EnumPresetTitle(18, "PRESET_TITLE_CUSTOM")
    public object PRESET_TITLE_AIR : EnumPresetTitle(19, "PRESET_TITLE_AIR")
    public object PRESET_TITLE_BIKE : EnumPresetTitle(20, "PRESET_TITLE_BIKE")
    public object PRESET_TITLE_EPIC : EnumPresetTitle(21, "PRESET_TITLE_EPIC")
    public object PRESET_TITLE_INDOOR : EnumPresetTitle(22, "PRESET_TITLE_INDOOR")
    public object PRESET_TITLE_MOTOR : EnumPresetTitle(23, "PRESET_TITLE_MOTOR")
    public object PRESET_TITLE_MOUNTED : EnumPresetTitle(24, "PRESET_TITLE_MOUNTED")
    public object PRESET_TITLE_OUTDOOR : EnumPresetTitle(25, "PRESET_TITLE_OUTDOOR")
    public object PRESET_TITLE_POV : EnumPresetTitle(26, "PRESET_TITLE_POV")
    public object PRESET_TITLE_SELFIE : EnumPresetTitle(27, "PRESET_TITLE_SELFIE")
    public object PRESET_TITLE_SKATE : EnumPresetTitle(28, "PRESET_TITLE_SKATE")
    public object PRESET_TITLE_SNOW : EnumPresetTitle(29, "PRESET_TITLE_SNOW")
    public object PRESET_TITLE_TRAIL : EnumPresetTitle(30, "PRESET_TITLE_TRAIL")
    public object PRESET_TITLE_TRAVEL : EnumPresetTitle(31, "PRESET_TITLE_TRAVEL")
    public object PRESET_TITLE_WATER : EnumPresetTitle(32, "PRESET_TITLE_WATER")
    public object PRESET_TITLE_LOOPING : EnumPresetTitle(33, "PRESET_TITLE_LOOPING")
    public object PRESET_TITLE_STARS : EnumPresetTitle(34, "PRESET_TITLE_STARS")
    public object PRESET_TITLE_ACTION : EnumPresetTitle(35, "PRESET_TITLE_ACTION")
    public object PRESET_TITLE_FOLLOW_CAM : EnumPresetTitle(36, "PRESET_TITLE_FOLLOW_CAM")
    public object PRESET_TITLE_SURF : EnumPresetTitle(37, "PRESET_TITLE_SURF")
    public object PRESET_TITLE_CITY : EnumPresetTitle(38, "PRESET_TITLE_CITY")
    public object PRESET_TITLE_SHAKY : EnumPresetTitle(39, "PRESET_TITLE_SHAKY")
    public object PRESET_TITLE_CHESTY : EnumPresetTitle(40, "PRESET_TITLE_CHESTY")
    public object PRESET_TITLE_HELMET : EnumPresetTitle(41, "PRESET_TITLE_HELMET")
    public object PRESET_TITLE_BITE : EnumPresetTitle(42, "PRESET_TITLE_BITE")
    public object PRESET_TITLE_CUSTOM_CINEMATIC : EnumPresetTitle(43, "PRESET_TITLE_CUSTOM_CINEMATIC")
    public object PRESET_TITLE_VLOG : EnumPresetTitle(44, "PRESET_TITLE_VLOG")
    public object PRESET_TITLE_FPV : EnumPresetTitle(45, "PRESET_TITLE_FPV")
    public object PRESET_TITLE_HDR : EnumPresetTitle(46, "PRESET_TITLE_HDR")
    public object PRESET_TITLE_LANDSCAPE : EnumPresetTitle(47, "PRESET_TITLE_LANDSCAPE")
    public object PRESET_TITLE_LOG : EnumPresetTitle(48, "PRESET_TITLE_LOG")
    public object PRESET_TITLE_CUSTOM_SLOMO : EnumPresetTitle(49, "PRESET_TITLE_CUSTOM_SLOMO")
    public object PRESET_TITLE_TRIPOD : EnumPresetTitle(50, "PRESET_TITLE_TRIPOD")
    public object PRESET_TITLE_BASIC : EnumPresetTitle(58, "PRESET_TITLE_BASIC")
    public object PRESET_TITLE_ULTRA_SLO_MO : EnumPresetTitle(59, "PRESET_TITLE_ULTRA_SLO_MO")
    public object PRESET_TITLE_STANDARD_ENDURANCE : EnumPresetTitle(60, "PRESET_TITLE_STANDARD_ENDURANCE")
    public object PRESET_TITLE_ACTIVITY_ENDURANCE : EnumPresetTitle(61, "PRESET_TITLE_ACTIVITY_ENDURANCE")
    public object PRESET_TITLE_CINEMATIC_ENDURANCE : EnumPresetTitle(62, "PRESET_TITLE_CINEMATIC_ENDURANCE")
    public object PRESET_TITLE_SLOMO_ENDURANCE : EnumPresetTitle(63, "PRESET_TITLE_SLOMO_ENDURANCE")
    public object PRESET_TITLE_STATIONARY_1 : EnumPresetTitle(64, "PRESET_TITLE_STATIONARY_1")
    public object PRESET_TITLE_STATIONARY_2 : EnumPresetTitle(65, "PRESET_TITLE_STATIONARY_2")
    public object PRESET_TITLE_STATIONARY_3 : EnumPresetTitle(66, "PRESET_TITLE_STATIONARY_3")
    public object PRESET_TITLE_STATIONARY_4 : EnumPresetTitle(67, "PRESET_TITLE_STATIONARY_4")
    public object PRESET_TITLE_SIMPLE_VIDEO : EnumPresetTitle(68, "PRESET_TITLE_SIMPLE_VIDEO")
    public object PRESET_TITLE_SIMPLE_TIME_WARP : EnumPresetTitle(69, "PRESET_TITLE_SIMPLE_TIME_WARP")
    public object PRESET_TITLE_SIMPLE_SUPER_PHOTO : EnumPresetTitle(70, "PRESET_TITLE_SIMPLE_SUPER_PHOTO")
    public object PRESET_TITLE_SIMPLE_NIGHT_PHOTO : EnumPresetTitle(71, "PRESET_TITLE_SIMPLE_NIGHT_PHOTO")
    public object PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE : EnumPresetTitle(72, "PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE")
    public object PRESET_TITLE_HIGHEST_QUALITY : EnumPresetTitle(73, "PRESET_TITLE_HIGHEST_QUALITY")
    public object PRESET_TITLE_EXTENDED_BATTERY : EnumPresetTitle(74, "PRESET_TITLE_EXTENDED_BATTERY")
    public object PRESET_TITLE_LONGEST_BATTERY : EnumPresetTitle(75, "PRESET_TITLE_LONGEST_BATTERY")
    public object PRESET_TITLE_STAR_TRAIL : EnumPresetTitle(76, "PRESET_TITLE_STAR_TRAIL")
    public object PRESET_TITLE_LIGHT_PAINTING : EnumPresetTitle(77, "PRESET_TITLE_LIGHT_PAINTING")
    public object PRESET_TITLE_LIGHT_TRAIL : EnumPresetTitle(78, "PRESET_TITLE_LIGHT_TRAIL")
    public object PRESET_TITLE_FULL_FRAME : EnumPresetTitle(79, "PRESET_TITLE_FULL_FRAME")
    public object PRESET_TITLE_STANDARD_QUALITY_VIDEO : EnumPresetTitle(82, "PRESET_TITLE_STANDARD_QUALITY_VIDEO")
    public object PRESET_TITLE_BASIC_QUALITY_VIDEO : EnumPresetTitle(83, "PRESET_TITLE_BASIC_QUALITY_VIDEO")
    public object PRESET_TITLE_HIGHEST_QUALITY_VIDEO : EnumPresetTitle(93, "PRESET_TITLE_HIGHEST_QUALITY_VIDEO")
    public object PRESET_TITLE_USER_DEFINED_CUSTOM_NAME : EnumPresetTitle(94, "PRESET_TITLE_USER_DEFINED_CUSTOM_NAME")
    public object PRESET_TITLE_EASY_STANDARD_PROFILE : EnumPresetTitle(99, "PRESET_TITLE_EASY_STANDARD_PROFILE")
    public object PRESET_TITLE_EASY_HDR_PROFILE : EnumPresetTitle(100, "PRESET_TITLE_EASY_HDR_PROFILE")
    public object PRESET_TITLE_BURST_SLOMO : EnumPresetTitle(106, "PRESET_TITLE_BURST_SLOMO")
    public class UNRECOGNIZED(value: Int) : EnumPresetTitle(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumPresetTitle> {
        public val values: List<open_gopro.EnumPresetTitle> by lazy { listOf(PRESET_TITLE_ACTIVITY, PRESET_TITLE_STANDARD, PRESET_TITLE_CINEMATIC, PRESET_TITLE_PHOTO, PRESET_TITLE_LIVE_BURST, PRESET_TITLE_BURST, PRESET_TITLE_NIGHT, PRESET_TITLE_TIME_WARP, PRESET_TITLE_TIME_LAPSE, PRESET_TITLE_NIGHT_LAPSE, PRESET_TITLE_VIDEO, PRESET_TITLE_SLOMO, PRESET_TITLE_PHOTO_2, PRESET_TITLE_PANORAMA, PRESET_TITLE_TIME_WARP_2, PRESET_TITLE_CUSTOM, PRESET_TITLE_AIR, PRESET_TITLE_BIKE, PRESET_TITLE_EPIC, PRESET_TITLE_INDOOR, PRESET_TITLE_MOTOR, PRESET_TITLE_MOUNTED, PRESET_TITLE_OUTDOOR, PRESET_TITLE_POV, PRESET_TITLE_SELFIE, PRESET_TITLE_SKATE, PRESET_TITLE_SNOW, PRESET_TITLE_TRAIL, PRESET_TITLE_TRAVEL, PRESET_TITLE_WATER, PRESET_TITLE_LOOPING, PRESET_TITLE_STARS, PRESET_TITLE_ACTION, PRESET_TITLE_FOLLOW_CAM, PRESET_TITLE_SURF, PRESET_TITLE_CITY, PRESET_TITLE_SHAKY, PRESET_TITLE_CHESTY, PRESET_TITLE_HELMET, PRESET_TITLE_BITE, PRESET_TITLE_CUSTOM_CINEMATIC, PRESET_TITLE_VLOG, PRESET_TITLE_FPV, PRESET_TITLE_HDR, PRESET_TITLE_LANDSCAPE, PRESET_TITLE_LOG, PRESET_TITLE_CUSTOM_SLOMO, PRESET_TITLE_TRIPOD, PRESET_TITLE_BASIC, PRESET_TITLE_ULTRA_SLO_MO, PRESET_TITLE_STANDARD_ENDURANCE, PRESET_TITLE_ACTIVITY_ENDURANCE, PRESET_TITLE_CINEMATIC_ENDURANCE, PRESET_TITLE_SLOMO_ENDURANCE, PRESET_TITLE_STATIONARY_1, PRESET_TITLE_STATIONARY_2, PRESET_TITLE_STATIONARY_3, PRESET_TITLE_STATIONARY_4, PRESET_TITLE_SIMPLE_VIDEO, PRESET_TITLE_SIMPLE_TIME_WARP, PRESET_TITLE_SIMPLE_SUPER_PHOTO, PRESET_TITLE_SIMPLE_NIGHT_PHOTO, PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE, PRESET_TITLE_HIGHEST_QUALITY, PRESET_TITLE_EXTENDED_BATTERY, PRESET_TITLE_LONGEST_BATTERY, PRESET_TITLE_STAR_TRAIL, PRESET_TITLE_LIGHT_PAINTING, PRESET_TITLE_LIGHT_TRAIL, PRESET_TITLE_FULL_FRAME, PRESET_TITLE_STANDARD_QUALITY_VIDEO, PRESET_TITLE_BASIC_QUALITY_VIDEO, PRESET_TITLE_HIGHEST_QUALITY_VIDEO, PRESET_TITLE_USER_DEFINED_CUSTOM_NAME, PRESET_TITLE_EASY_STANDARD_PROFILE, PRESET_TITLE_EASY_HDR_PROFILE, PRESET_TITLE_BURST_SLOMO) }
        override fun fromValue(value: Int): open_gopro.EnumPresetTitle = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumPresetTitle = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumPresetTitle with name: $name")
    }
}

@pbandk.Export
public data class NotifyPresetStatus(
    val presetGroupArray: List<open_gopro.PresetGroup> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.NotifyPresetStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyPresetStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.NotifyPresetStatus> {
        public val defaultInstance: open_gopro.NotifyPresetStatus by lazy { open_gopro.NotifyPresetStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.NotifyPresetStatus = open_gopro.NotifyPresetStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyPresetStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyPresetStatus",
            messageClass = open_gopro.NotifyPresetStatus::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "preset_group_array",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.PresetGroup>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = open_gopro.PresetGroup.Companion)),
                        jsonName = "presetGroupArray",
                        value = open_gopro.NotifyPresetStatus::presetGroupArray
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class Preset(
    val id: Int? = null,
    val mode: open_gopro.EnumFlatMode? = null,
    val titleId: open_gopro.EnumPresetTitle? = null,
    val titleNumber: Int? = null,
    val userDefined: Boolean? = null,
    val icon: open_gopro.EnumPresetIcon? = null,
    val settingArray: List<open_gopro.PresetSetting> = emptyList(),
    val isModified: Boolean? = null,
    val isFixed: Boolean? = null,
    val customName: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.Preset = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.Preset> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.Preset> {
        public val defaultInstance: open_gopro.Preset by lazy { open_gopro.Preset() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.Preset = open_gopro.Preset.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.Preset> = pbandk.MessageDescriptor(
            fullName = "open_gopro.Preset",
            messageClass = open_gopro.Preset::class,
            messageCompanion = this,
            fields = buildList(10) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "id",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "id",
                        value = open_gopro.Preset::id
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "mode",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumFlatMode.Companion, hasPresence = true),
                        jsonName = "mode",
                        value = open_gopro.Preset::mode
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "title_id",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetTitle.Companion, hasPresence = true),
                        jsonName = "titleId",
                        value = open_gopro.Preset::titleId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "title_number",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "titleNumber",
                        value = open_gopro.Preset::titleNumber
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "user_defined",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "userDefined",
                        value = open_gopro.Preset::userDefined
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "icon",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetIcon.Companion, hasPresence = true),
                        jsonName = "icon",
                        value = open_gopro.Preset::icon
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "setting_array",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.PresetSetting>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = open_gopro.PresetSetting.Companion)),
                        jsonName = "settingArray",
                        value = open_gopro.Preset::settingArray
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "is_modified",
                        number = 8,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "isModified",
                        value = open_gopro.Preset::isModified
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "is_fixed",
                        number = 9,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "isFixed",
                        value = open_gopro.Preset::isFixed
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "custom_name",
                        number = 10,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "customName",
                        value = open_gopro.Preset::customName
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestCustomPresetUpdate(
    val titleId: open_gopro.EnumPresetTitle? = null,
    val customName: String? = null,
    val iconId: open_gopro.EnumPresetIcon? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestCustomPresetUpdate = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCustomPresetUpdate> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestCustomPresetUpdate> {
        public val defaultInstance: open_gopro.RequestCustomPresetUpdate by lazy { open_gopro.RequestCustomPresetUpdate() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestCustomPresetUpdate = open_gopro.RequestCustomPresetUpdate.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCustomPresetUpdate> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCustomPresetUpdate",
            messageClass = open_gopro.RequestCustomPresetUpdate::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "title_id",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetTitle.Companion, hasPresence = true),
                        jsonName = "titleId",
                        value = open_gopro.RequestCustomPresetUpdate::titleId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "custom_name",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "customName",
                        value = open_gopro.RequestCustomPresetUpdate::customName
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "icon_id",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetIcon.Companion, hasPresence = true),
                        jsonName = "iconId",
                        value = open_gopro.RequestCustomPresetUpdate::iconId
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class PresetGroup(
    val id: open_gopro.EnumPresetGroup? = null,
    val presetArray: List<open_gopro.Preset> = emptyList(),
    val canAddPreset: Boolean? = null,
    val icon: open_gopro.EnumPresetGroupIcon? = null,
    val modeArray: List<open_gopro.EnumFlatMode> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.PresetGroup = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.PresetGroup> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.PresetGroup> {
        public val defaultInstance: open_gopro.PresetGroup by lazy { open_gopro.PresetGroup() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.PresetGroup = open_gopro.PresetGroup.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.PresetGroup> = pbandk.MessageDescriptor(
            fullName = "open_gopro.PresetGroup",
            messageClass = open_gopro.PresetGroup::class,
            messageCompanion = this,
            fields = buildList(5) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "id",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetGroup.Companion, hasPresence = true),
                        jsonName = "id",
                        value = open_gopro.PresetGroup::id
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "preset_array",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.Preset>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = open_gopro.Preset.Companion)),
                        jsonName = "presetArray",
                        value = open_gopro.PresetGroup::presetArray
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "can_add_preset",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "canAddPreset",
                        value = open_gopro.PresetGroup::canAddPreset
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "icon",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumPresetGroupIcon.Companion, hasPresence = true),
                        jsonName = "icon",
                        value = open_gopro.PresetGroup::icon
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "mode_array",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumFlatMode>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumFlatMode.Companion)),
                        jsonName = "modeArray",
                        value = open_gopro.PresetGroup::modeArray
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class PresetSetting(
    val id: Int? = null,
    val value: Int? = null,
    val isCaption: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.PresetSetting = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.PresetSetting> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.PresetSetting> {
        public val defaultInstance: open_gopro.PresetSetting by lazy { open_gopro.PresetSetting() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.PresetSetting = open_gopro.PresetSetting.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.PresetSetting> = pbandk.MessageDescriptor(
            fullName = "open_gopro.PresetSetting",
            messageClass = open_gopro.PresetSetting::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "id",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "id",
                        value = open_gopro.PresetSetting::id
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "value",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "value",
                        value = open_gopro.PresetSetting::value
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "is_caption",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "isCaption",
                        value = open_gopro.PresetSetting::isCaption
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyPresetStatus")
public fun NotifyPresetStatus?.orDefault(): open_gopro.NotifyPresetStatus = this ?: NotifyPresetStatus.defaultInstance

private fun NotifyPresetStatus.protoMergeImpl(plus: pbandk.Message?): NotifyPresetStatus = (plus as? NotifyPresetStatus)?.let {
    it.copy(
        presetGroupArray = presetGroupArray + plus.presetGroupArray,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyPresetStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifyPresetStatus {
    var presetGroupArray: pbandk.ListWithSize.Builder<open_gopro.PresetGroup>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> presetGroupArray = (presetGroupArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.PresetGroup> }
        }
    }

    return NotifyPresetStatus(pbandk.ListWithSize.Builder.fixed(presetGroupArray), unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPreset")
public fun Preset?.orDefault(): open_gopro.Preset = this ?: Preset.defaultInstance

private fun Preset.protoMergeImpl(plus: pbandk.Message?): Preset = (plus as? Preset)?.let {
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
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun Preset.Companion.decodeWithImpl(u: pbandk.MessageDecoder): Preset {
    var id: Int? = null
    var mode: open_gopro.EnumFlatMode? = null
    var titleId: open_gopro.EnumPresetTitle? = null
    var titleNumber: Int? = null
    var userDefined: Boolean? = null
    var icon: open_gopro.EnumPresetIcon? = null
    var settingArray: pbandk.ListWithSize.Builder<open_gopro.PresetSetting>? = null
    var isModified: Boolean? = null
    var isFixed: Boolean? = null
    var customName: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> id = _fieldValue as Int
            2 -> mode = _fieldValue as open_gopro.EnumFlatMode
            3 -> titleId = _fieldValue as open_gopro.EnumPresetTitle
            4 -> titleNumber = _fieldValue as Int
            5 -> userDefined = _fieldValue as Boolean
            6 -> icon = _fieldValue as open_gopro.EnumPresetIcon
            7 -> settingArray = (settingArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.PresetSetting> }
            8 -> isModified = _fieldValue as Boolean
            9 -> isFixed = _fieldValue as Boolean
            10 -> customName = _fieldValue as String
        }
    }

    return Preset(id, mode, titleId, titleNumber,
        userDefined, icon, pbandk.ListWithSize.Builder.fixed(settingArray), isModified,
        isFixed, customName, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCustomPresetUpdate")
public fun RequestCustomPresetUpdate?.orDefault(): open_gopro.RequestCustomPresetUpdate = this ?: RequestCustomPresetUpdate.defaultInstance

private fun RequestCustomPresetUpdate.protoMergeImpl(plus: pbandk.Message?): RequestCustomPresetUpdate = (plus as? RequestCustomPresetUpdate)?.let {
    it.copy(
        titleId = plus.titleId ?: titleId,
        customName = plus.customName ?: customName,
        iconId = plus.iconId ?: iconId,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCustomPresetUpdate.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestCustomPresetUpdate {
    var titleId: open_gopro.EnumPresetTitle? = null
    var customName: String? = null
    var iconId: open_gopro.EnumPresetIcon? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> titleId = _fieldValue as open_gopro.EnumPresetTitle
            2 -> customName = _fieldValue as String
            3 -> iconId = _fieldValue as open_gopro.EnumPresetIcon
        }
    }

    return RequestCustomPresetUpdate(titleId, customName, iconId, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPresetGroup")
public fun PresetGroup?.orDefault(): open_gopro.PresetGroup = this ?: PresetGroup.defaultInstance

private fun PresetGroup.protoMergeImpl(plus: pbandk.Message?): PresetGroup = (plus as? PresetGroup)?.let {
    it.copy(
        id = plus.id ?: id,
        presetArray = presetArray + plus.presetArray,
        canAddPreset = plus.canAddPreset ?: canAddPreset,
        icon = plus.icon ?: icon,
        modeArray = modeArray + plus.modeArray,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun PresetGroup.Companion.decodeWithImpl(u: pbandk.MessageDecoder): PresetGroup {
    var id: open_gopro.EnumPresetGroup? = null
    var presetArray: pbandk.ListWithSize.Builder<open_gopro.Preset>? = null
    var canAddPreset: Boolean? = null
    var icon: open_gopro.EnumPresetGroupIcon? = null
    var modeArray: pbandk.ListWithSize.Builder<open_gopro.EnumFlatMode>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> id = _fieldValue as open_gopro.EnumPresetGroup
            2 -> presetArray = (presetArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.Preset> }
            3 -> canAddPreset = _fieldValue as Boolean
            4 -> icon = _fieldValue as open_gopro.EnumPresetGroupIcon
            5 -> modeArray = (modeArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumFlatMode> }
        }
    }

    return PresetGroup(id, pbandk.ListWithSize.Builder.fixed(presetArray), canAddPreset, icon,
        pbandk.ListWithSize.Builder.fixed(modeArray), unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForPresetSetting")
public fun PresetSetting?.orDefault(): open_gopro.PresetSetting = this ?: PresetSetting.defaultInstance

private fun PresetSetting.protoMergeImpl(plus: pbandk.Message?): PresetSetting = (plus as? PresetSetting)?.let {
    it.copy(
        id = plus.id ?: id,
        value = plus.value ?: value,
        isCaption = plus.isCaption ?: isCaption,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun PresetSetting.Companion.decodeWithImpl(u: pbandk.MessageDecoder): PresetSetting {
    var id: Int? = null
    var value: Int? = null
    var isCaption: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> id = _fieldValue as Int
            2 -> value = _fieldValue as Int
            3 -> isCaption = _fieldValue as Boolean
        }
    }

    return PresetSetting(id, value, isCaption, unknownFields)
}
