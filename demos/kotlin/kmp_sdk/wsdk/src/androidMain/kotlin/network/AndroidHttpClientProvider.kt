package network

import di.createHttpClient
import domain.network.IHttpClientProvider
import entity.network.IHttpsCredentials
import io.ktor.client.HttpClient
import io.ktor.client.engine.okhttp.OkHttp
import okhttp3.Credentials
import okhttp3.Interceptor
import okio.Buffer
import java.security.KeyStore
import java.security.cert.CertificateFactory
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManagerFactory
import javax.net.ssl.X509TrustManager

object AndroidHttpClientProvider : IHttpClientProvider {
    override fun provideBaseClient(credentials: IHttpsCredentials?): HttpClient =
        credentials?.let {
            // Build X509 certificates from string certificates
            val certificates = credentials.certificates.map { cert ->
                CertificateFactory.getInstance("X.509")
                    .generateCertificates(Buffer().writeUtf8(cert).inputStream())
                    .first()
            }
            // Put the certificate(s) in a key store.
            val keyStore = KeyStore.getInstance(KeyStore.getDefaultType()).apply {
                load(null, "password".toCharArray()) // Any password will work.
                certificates.forEachIndexed { index, certificate ->
                    setCertificateEntry(index.toString(), certificate)
                }
            }
            // Use the key store to build an X509 trust manager.
            val trustManager =
                TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm())
                    .apply { init(keyStore) }
                    .trustManagers.first() as X509TrustManager
            // Build socket factory from trust manager
            val httpsSslSocketFactory = SSLContext.getInstance("TLS")
                .apply { init(null, arrayOf(trustManager), null) }
                .socketFactory
            // Add interceptor to append basic auth credentials to request headers
            val httpsAuthInterceptor = Interceptor { chain ->
                chain.request().newBuilder().run {
                    header(
                        "Authorization",
                        Credentials.basic(credentials.username, credentials.password)
                    )
                    build()
                }.let { chain.proceed(it) }
            }

            val engine = OkHttp.create {
                config {
                    addInterceptor(httpsAuthInterceptor)
                    sslSocketFactory(httpsSslSocketFactory, trustManager)
                }
            }
            createHttpClient(engine)
        } ?: createHttpClient(OkHttp.create())
}
