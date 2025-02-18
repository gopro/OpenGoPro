package com.gopro.open_gopro.operations

import kotlinx.serialization.Serializable

@Serializable
data class OgpVersionHttpResponse(
    val version: String
)