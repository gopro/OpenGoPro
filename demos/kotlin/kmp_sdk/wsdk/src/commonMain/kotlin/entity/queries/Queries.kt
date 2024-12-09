package entity.queries

interface IValuedEnum<T> {
    val value: T
}

@OptIn(ExperimentalUnsignedTypes::class)
interface IUByteArrayCompanion<T> where T : Enum<T>, T : IValuedEnum<*> {
    fun fromUByteArray(value: UByteArray): T
}

enum class BooleanEnum(override val value: UByte) : IValuedEnum<UByte> {
    FALSE(0U),
    TRUE(1U);

    fun toBoolean() = this == TRUE

    @OptIn(ExperimentalUnsignedTypes::class)
    companion object : IUByteArrayCompanion<BooleanEnum> {
        override fun fromUByteArray(value: UByteArray) = BooleanEnum.entries.first { it.value == value.last() }
    }
}

enum class StatusId(override val value: UByte) : IValuedEnum<UByte> {
    IS_BUSY(8U),
    IS_ENCODING(10U),
    BATTERY_LEVEL(70U);

    @OptIn(ExperimentalUnsignedTypes::class)
    companion object : IUByteArrayCompanion<StatusId> {
        override fun fromUByteArray(value: UByteArray) = entries.first { it.value == value.last() }
    }
}
