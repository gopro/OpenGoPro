package com.gopro.open_gopro.entity.operation

data class ApScanResult(
    val scanId: Int?,
    val totalEntries: Int?,
    val totalConfiguredSsids: Int?
)

data class ApScanEntry(
    val ssid: String,
    val signalStrengthBars: Int,
    val signalFrequencyMhz: Int,
    val isOpen: Boolean,
    val isAuthenticated: Boolean,
    val isConfigured: Boolean,
    val isBestSsid: Boolean,
    val isAssociated: Boolean,
)

sealed class AccessPointState {
    data object Disconnected : AccessPointState()
    data class InProgress(val ssid: String) : AccessPointState()
    data class Connected(val ssid: String) : AccessPointState()
}

fun AccessPointState.isFinished(): Boolean = when (this) {
    AccessPointState.Disconnected, is AccessPointState.Connected -> true
    else -> false
}