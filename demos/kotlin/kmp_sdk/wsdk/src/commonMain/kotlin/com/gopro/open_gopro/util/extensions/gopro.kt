package com.gopro.open_gopro.util.extensions

import com.gopro.open_gopro.CommunicationType

internal fun List<CommunicationType>.bleIfAvailable(): CommunicationType? =
    this.firstOrNull { it == CommunicationType.BLE }

internal fun List<CommunicationType>.httpIfAvailable(): CommunicationType? =
    this.firstOrNull { (it == CommunicationType.HTTP) }