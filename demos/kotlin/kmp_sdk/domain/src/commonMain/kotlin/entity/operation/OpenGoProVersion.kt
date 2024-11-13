package entity.operation

import kotlinx.serialization.Serializable

@Serializable
data class OgpVersionHttpResponse(
    val version: String
)