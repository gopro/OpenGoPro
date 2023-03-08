/* Wifi.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.network

import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiManager
import android.net.wifi.WifiNetworkSpecifier
import android.provider.Settings
import com.example.open_gopro_tutorial.util.prettyJson
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.util.cio.*
import io.ktor.utils.io.*
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonObject
import timber.log.Timber
import java.io.File
import java.lang.ref.WeakReference
import kotlin.coroutines.Continuation
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine


class WifiEventListener {
    var onDisconnect: ((Network) -> Unit)? = null
    var onConnect: ((Network) -> Unit)? = null
}

class Wifi(private val context: Context) {
    lateinit var continuation: Continuation<Unit>
    private val listeners: MutableSet<WeakReference<WifiEventListener>> = mutableSetOf()

    private val wifiManager: WifiManager by lazy { context.getSystemService(Context.WIFI_SERVICE) as WifiManager }
    private val connectivityManager by lazy {
        context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    }

    fun enableAdapter() {
        if (!wifiManager.isWifiEnabled) {
            val panelIntent = Intent(Settings.Panel.ACTION_INTERNET_CONNECTIVITY)
            panelIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(panelIntent)
        }
    }

    private val client by lazy {
        HttpClient(CIO) {
            install(HttpTimeout)
        }
    }

    private val callback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            super.onAvailable(network)
            // Note!! this prevents us from using LTE / the internet
            connectivityManager.bindProcessToNetwork(network)
            this@Wifi.continuation.resume(Unit)
            listeners.forEach { it.get()?.onConnect?.run { this(network) } }
        }

        override fun onLost(network: Network) {
            Timber.d("Lost network $network")
            super.onLost(network)
            connectivityManager.bindProcessToNetwork(null)
            connectivityManager.unregisterNetworkCallback(this)
            listeners.forEach { it.get()?.onDisconnect?.run { this(network) } }
        }
    }

    fun registerListener(listener: WifiEventListener) {
        listeners.add(WeakReference(listener))
    }

    // TODO unregister and handle removing cleaned up weak references

    suspend fun connect(ssid: String, password: String) {
        val wifiNetworkSpecifier =
            WifiNetworkSpecifier.Builder().setSsid(ssid).setWpa2Passphrase(password).build()

        val networkRequest =
            NetworkRequest.Builder().addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
                .setNetworkSpecifier(wifiNetworkSpecifier).build()

        val connectivityManager =
            context.applicationContext.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager?

        Timber.d("Connecting to Wifi...")
        suspendCoroutine { cont ->
            this.continuation = cont
            connectivityManager?.requestNetwork(networkRequest, callback)
        }
        Timber.d("Wifi connected")
    }

    suspend fun get(endpoint: String, timeoutMs: Long = 5000L): JsonObject {
        Timber.d("GET request to: $endpoint")
        val response = client.request(endpoint) {
            timeout {
                requestTimeoutMillis = timeoutMs
            }
        }
        val bodyAsString: String = response.body()
        return prettyJson.parseToJsonElement(bodyAsString).jsonObject
    }

    suspend fun getFile(
        endpoint: String, context: Context, file: File? = null, timeoutMs: Long = 10000L
    ): File {
        val destination = file ?: File(context.filesDir, endpoint.split("/").last())
        val response = client.request(endpoint) {
            timeout {
                requestTimeoutMillis = timeoutMs
            }
        }
        response.bodyAsChannel().copyAndClose(destination.writeChannel())
        return destination
    }
}