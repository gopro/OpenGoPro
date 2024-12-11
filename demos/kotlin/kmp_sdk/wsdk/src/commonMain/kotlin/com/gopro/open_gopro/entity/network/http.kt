package com.gopro.open_gopro.entity.network

import kotlinx.serialization.Serializable

internal interface IHttpsCredentials {
    val username: String
    val password: String
    val certificates: List<String>
}

@Serializable
internal data class HttpsCredentials(
    override val username: String,
    override val password: String,
    override val certificates: List<String>
): IHttpsCredentials