/* AndroidHttpClientProvider.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.network

import com.gopro.open_gopro.di.createHttpClient
import com.gopro.open_gopro.domain.network.IHttpClientProvider
import com.gopro.open_gopro.entity.network.IHttpsCredentials
import io.ktor.client.HttpClient
import io.ktor.client.engine.okhttp.OkHttp
import java.security.KeyStore
import java.security.cert.CertificateFactory
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManagerFactory
import javax.net.ssl.X509TrustManager
import okhttp3.Credentials
import okhttp3.Interceptor
import okio.Buffer

internal object AndroidHttpClientProvider : IHttpClientProvider {
  override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient =
      credentials?.let {
        // Build X509 certificates from string certificates
        val certificates =
            credentials.certificates.map { cert ->
              CertificateFactory.getInstance("X.509")
                  .generateCertificates(Buffer().writeUtf8(cert).inputStream())
                  .first()
            }
        // Put the certificate(s) in a key store.
        val keyStore =
            KeyStore.getInstance(KeyStore.getDefaultType()).apply {
              load(null, "password".toCharArray()) // Any password will work.
              certificates.forEachIndexed { index, certificate ->
                setCertificateEntry(index.toString(), certificate)
              }
            }
        // Use the key store to build an X509 trust manager.
        val trustManager =
            TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm())
                .apply { init(keyStore) }
                .trustManagers
                .first() as X509TrustManager
        // Build socket factory from trust manager
        val httpsSslSocketFactory =
            SSLContext.getInstance("TLS")
                .apply { init(null, arrayOf(trustManager), null) }
                .socketFactory
        // Add interceptor to append basic auth credentials to request headers
        val httpsAuthInterceptor = Interceptor { chain ->
          chain
              .request()
              .newBuilder()
              .run {
                header(
                    "Authorization", Credentials.basic(credentials.username, credentials.password))
                build()
              }
              .let { chain.proceed(it) }
        }

        val engine =
            OkHttp.create {
              config {
                addInterceptor(httpsAuthInterceptor)
                sslSocketFactory(httpsSslSocketFactory, trustManager)
              }
            }
        createHttpClient(engine)
      } ?: createHttpClient(OkHttp.create())
}
