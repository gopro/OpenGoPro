/* httpClient.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.di

import com.gopro.open_gopro.operations.jsonDefault
import io.ktor.client.HttpClient
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.logging.Logging
import io.ktor.serialization.kotlinx.json.json

internal fun createHttpClient(
    engine: HttpClientEngine,
): HttpClient {
  val kermit = co.touchlab.kermit.Logger.withTag("Ktor")
  val client =
      HttpClient(engine) {
        install(ContentNegotiation) {
          json(
              json = jsonDefault // Use our custom serializer to handle protobuf enums
              )
        }
        install(Logging) {
          level = LogLevel.ALL

          logger =
              object : Logger {
                override fun log(message: String) {
                  kermit.i { message }
                }
              }
        }
      }

  return client
}
