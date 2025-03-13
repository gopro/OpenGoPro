/* gopro.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util.extensions

import com.gopro.open_gopro.CommunicationType

internal fun List<CommunicationType>.bleIfAvailable(): CommunicationType? =
    this.firstOrNull { it == CommunicationType.BLE }

internal fun List<CommunicationType>.httpIfAvailable(): CommunicationType? =
    this.firstOrNull { (it == CommunicationType.HTTP) }
