/* http.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

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
) : IHttpsCredentials
