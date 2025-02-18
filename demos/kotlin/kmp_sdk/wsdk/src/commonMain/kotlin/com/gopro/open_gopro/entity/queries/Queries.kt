/* Queries.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

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

