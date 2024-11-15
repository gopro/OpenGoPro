package entity.queries

interface UByteEnum {
    val value: UByte
}

interface IUByteEnumCompanion<T> where T : Enum<T>, T : UByteEnum {
    fun fromUByte(value: UByte): T
}

enum class BooleanEnum(override val value: UByte) : UByteEnum {
    FALSE(0U),
    TRUE(1U);

    fun toBoolean() = this == TRUE

    companion object : IUByteEnumCompanion<BooleanEnum> {
        override fun fromUByte(value: UByte) = BooleanEnum.entries.first { it.value == value }
    }
}

// TODO these need to be automatically generated

/**
 * Video Resolution
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)
 *
 * @property value
 */
enum class Resolution(override val value: UByte) : UByteEnum {
    RES_4K(1U),
    RES_2_7K(4U),
    RES_2_7K_4_3(6U),
    RES_1440(7U),
    RES_1080(9U),
    RES_720(12U),
    RES_4K_4_3(18U),
    RES_5_6K(21U),
    RES_5K(24U),
    RES_5K_4_3(25U),
    RES_5_3K_8_7(26U),
    RES_5_3K_4_3(27U),
    RES_4K_8_7(28U),
    RES_8K(31U),
    RES_4_8K(33U),
    RES_5_3K_1_9(35U),
    RES_4K_1_9(36U),
    RES_4K_1_1(37U),
    RES_900(38U),
    RES_4K_SPH(39U),
    RES_5_3K(100U),
    RES_5_3K_8_7_V2(107U),
    RES_4K_8_7_V2(108U),
    RES_4K_9_16_V2(109U),
    RES_1080_9_16_V2(110U),
    RES_2_7K_4_3_V2(111U);

    companion object : IUByteEnumCompanion<Resolution> {
        override fun fromUByte(value: UByte) = Resolution.entries.first { it.value == value }
    }
}

enum class Fps(override val value: UByte) : UByteEnum {
    FPS_30(0U),
    FPS_90(1U);

    companion object : IUByteEnumCompanion<Fps> {
        override fun fromUByte(value: UByte): Fps = entries.first { it.value == value }
    }
}

enum class VideoLens(override val value: UByte) : UByteEnum {
    WIDE(0U);

    companion object : IUByteEnumCompanion<VideoLens> {
        override fun fromUByte(value: UByte): VideoLens = entries.first { it.value == value }
    }
}


enum class SettingId(override val value: UByte) : UByteEnum {
    RESOLUTION(2U),
    FPS(3U),
    LED(91U),
    VIDEO_LENS(121U);

    companion object : IUByteEnumCompanion<SettingId> {
        override fun fromUByte(value: UByte) = entries.first { it.value == value }
    }
}

enum class StatusId(override val value: UByte) : UByteEnum {
    IS_BUSY(8U),
    IS_ENCODING(10U);

    companion object : IUByteEnumCompanion<StatusId> {
        override fun fromUByte(value: UByte) = entries.first { it.value == value }
    }
}
