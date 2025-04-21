/* Queries.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

interface IValuedEnum<T> {
  val value: T
}

@OptIn(ExperimentalUnsignedTypes::class)
interface IUByteArrayCompanion<T> {
  fun fromUByteArray(value: UByteArray): T

  fun toUByteArray(value: T): UByteArray
}
