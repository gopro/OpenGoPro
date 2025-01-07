/* Ble.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Mon Mar  6 17:45:14 UTC 2023 */

package com.example.open_gopro_tutorial.network

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.*
import android.bluetooth.le.*
import android.content.Context
import android.content.Intent
import android.content.Intent.FLAG_ACTIVITY_NEW_TASK
import android.os.Build
import androidx.annotation.RequiresPermission
import com.example.open_gopro_tutorial.*
import com.example.open_gopro_tutorial.util.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import timber.log.Timber
import java.lang.ref.WeakReference
import java.util.*
import java.util.concurrent.ConcurrentHashMap
import kotlin.coroutines.Continuation


private const val BLE_BASE_UUID = "0000%s-0000-1000-8000-00805F9B34FB"

enum class CoreUUID(val uuid: UUID) {
    CCC_DESCRIPTOR(UUID.fromString(BLE_BASE_UUID.format("2902"))), BATT_LEVEL(
        UUID.fromString(
            BLE_BASE_UUID.format("2a19")
        )
    )
}

@OptIn(ExperimentalUnsignedTypes::class)
class BleEventListener {
    var onNotification: ((UUID, UByteArray) -> Unit)? = null
    var onDisconnect: ((BluetoothDevice) -> Unit)? = null
    var onConnect: ((BluetoothDevice) -> Unit)? = null
}

/**
 * A per-context Bluetooth wrapper
 *
 * @property context context of this bluetooth wrapper
 */
class Bluetooth private constructor(private val context: Context) {
    companion object {
        private val instances: MutableMap<Context, Bluetooth> = mutableMapOf()

        fun getInstance(context: Context): Bluetooth = instances[context] ?: Bluetooth(context)

        val permissionsNeeded: List<String> by lazy {
            when {
                else -> listOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.BLUETOOTH_SCAN,
                    Manifest.permission.BLUETOOTH_CONNECT
                )
            }
        }
    }

    private val adapter: BluetoothAdapter by lazy {
        (context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter
            ?: throw Exception("Not able to acquire Bluetooth Adapter")
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    fun enableAdapter() {
        if (!adapter.isEnabled) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            enableBtIntent.addFlags(FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(enableBtIntent)
        }
    }

    private val scanner: BluetoothLeScanner by lazy {
        // This is a singleton but multiple scans can happen simultaneously by using different scan callbacks
        adapter.bluetoothLeScanner
    }

    data class DeviceEntry(
        var gatt: BluetoothGatt,
        var listeners: MutableSet<WeakReference<BleEventListener>> = mutableSetOf()
    )

    @OptIn(ExperimentalUnsignedTypes::class)
    sealed class BleJob<T> {
        companion object {
            // Only one Gatt operation can occur simultaneously (not including asynchronous notifications)
            private val mutex = Mutex()
        }

        private var continuation: Continuation<T>? = null

        suspend fun suspendWithTimeout(timeout: Long, action: () -> Any): Result<T> {
            mutex.withLock {
                try {
                    val returnValue = withTimeout(timeout) {
                        suspendCancellableCoroutine { cont ->
                            continuation = cont
                            try {
                                action()
                            } catch (e: Exception) {
                                continuation?.resumeWith(Result.failure(e))
                            }
                        }
                    }
                    continuation = null
                    return Result.success(returnValue)
                } catch (e: TimeoutCancellationException) {
                    continuation = null
                    return Result.failure(e)
                }
            }
        }

        fun resumeWithError(error: String) {
            Timber.d(error)
            continuation?.resumeWith(Result.failure((Exception(error))))
                ?: throw Exception("No current continuation")
        }

        fun resumeWithSuccess(value: T) = continuation?.resumeWith(Result.success(value))
            ?: throw Exception("No current continuation")

        object Connect : BleJob<BluetoothGatt>()
        object DiscoverServices : BleJob<Unit>()
        object Read : BleJob<UByteArray>()
        object Write : BleJob<Unit>()
        object EnableNotification : BleJob<Unit>()
    }

    private var genericListeners: MutableSet<WeakReference<BleEventListener>> = mutableSetOf()
    private var deviceGattMap = ConcurrentHashMap<BluetoothDevice, DeviceEntry>()
    private val scanObserverMap = ConcurrentHashMap<Int, ScanCallback>()

    /**
     * Private helper functions
     */
    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    private fun teardownConnection(device: BluetoothDevice) {
        if (device.isConnected()) {
            Timber.d("Disconnecting from ${device.address}")
            val deviceEntry = deviceGattMap.getValue(device)
            deviceEntry.gatt.close()
            // Notify registered listeners
            deviceEntry.listeners.forEach { it.get()?.onDisconnect?.invoke(device) }
            // Notify generic listeners
            genericListeners.forEach { it.get()?.onDisconnect?.invoke(device) }
            deviceGattMap.remove(device)
        } else {
            BleJob.Connect.resumeWithError("Connection failed during establishment")
            Timber.d("Not connected to ${device.address}, cannot teardown connection!")
        }
    }

    private fun deviceFromAddress(deviceAddress: String): BluetoothDevice? =
        BluetoothAdapter.checkBluetoothAddress(deviceAddress)
            .let { if (it) adapter.getRemoteDevice(deviceAddress) else null }


    private fun gattFromAddress(deviceAddress: String): BluetoothGatt? =
        deviceFromAddress(deviceAddress)?.let { deviceGattMap[it]?.gatt }


    private fun charFromUuid(
        gatt: BluetoothGatt, characteristic: UUID
    ): BluetoothGattCharacteristic? = gatt.findCharacteristic(characteristic)

    @SuppressLint("NewApi")
    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    fun writeCharacteristic(gatt: BluetoothGatt, char: BluetoothGattCharacteristic, payload: ByteArray, writeType: Int): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            gatt.writeCharacteristic(char, payload, writeType) == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION")
            char.value = payload
            char.writeType = writeType
            @Suppress("DEPRECATION")
            gatt.writeCharacteristic(char)
        }
    }

    @SuppressLint("NewApi")
    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    fun writeDescriptor(gatt: BluetoothGatt, descriptor: BluetoothGattDescriptor, payload: ByteArray): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            gatt.writeDescriptor(descriptor, payload) == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION")
            descriptor.value = payload
            @Suppress("DEPRECATION")
            gatt.writeDescriptor(descriptor)
        }
    }

    /**
     * Callbacks
     */
    private open class ScanCallbackWrapper(val flow: MutableSharedFlow<ScanResult>) : ScanCallback()

    private fun scanCallbackFactory(observer: MutableSharedFlow<ScanResult>) =
        object : ScanCallbackWrapper(observer) {
            override fun onScanFailed(errorCode: Int) {
                TODO("Handle error")
            }

            @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
            override fun onScanResult(callbackType: Int, result: ScanResult?) {
                Timber.d("Received scan result: ${result?.device?.name ?: ""}")
                result?.let {
                    runBlocking {
                        flow.emit(it)
                    }
                }
            }
        }


    @OptIn(ExperimentalUnsignedTypes::class)
    private val connectedCallback = object : BluetoothGattCallback() {
        @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
        override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
            val deviceAddress = gatt.device.address
            if (status == BluetoothGatt.GATT_SUCCESS) {
                if (newState == BluetoothProfile.STATE_CONNECTED) {
                    Timber.d("onConnectionStateChange: connected to $deviceAddress")
                    BleJob.Connect.resumeWithSuccess(gatt)
                    // Notify generic listeners
                    genericListeners.forEach { it.get()?.onConnect?.invoke(gatt.device) }
                } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                    Timber.d("onConnectionStateChange: disconnected from $deviceAddress")
                    teardownConnection(gatt.device)
                } else {
                    TODO("Not handled")
                }
            } else {
                Timber.d("onConnectionStateChange: status $status encountered for $deviceAddress!")
                teardownConnection(gatt.device)
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
            with(gatt) {
                if (status == BluetoothGatt.GATT_SUCCESS) {
                    Timber.d("Discovered ${services.size} services for ${gatt.device.address}")
                    printGattTable()
                    BleJob.DiscoverServices.resumeWithSuccess(Unit)
                } else {
                    BleJob.DiscoverServices.resumeWithError("Service discovery failed due to status $status")
                }
            }
        }

        @Deprecated("Deprecated for Android 13+",
            ReplaceWith("onCharacteristicRead(gatt, characteristic, characteristic.value, status)")
        )
        @Suppress("DEPRECATION")
        override fun onCharacteristicRead(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            status: Int,
        ) {
            onCharacteristicRead(gatt, characteristic, characteristic.value, status)
        }

        override fun onCharacteristicRead(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            value: ByteArray,
            status: Int
        ) {
            when (status) {
                BluetoothGatt.GATT_SUCCESS -> {
                    Timber.d("Read characteristic ${characteristic.uuid} : value: ${value.toHexString()}")
                    BleJob.Read.resumeWithSuccess(value.toUByteArray())
                }
                else -> {
                    BleJob.Read.resumeWithError("Characteristic read failed for $characteristic.uuid, error: $status")
                }
            }
        }

        override fun onCharacteristicWrite(
            gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic, status: Int
        ) {
            when (status) {
                BluetoothGatt.GATT_SUCCESS -> {
                    Timber.d("Wrote characteristic ${characteristic.uuid}")
                    BleJob.Write.resumeWithSuccess(Unit)
                }
                else -> {
                    BleJob.Write.resumeWithError("Characteristic write failed for ${characteristic.uuid}, error: $status")
                }
            }
        }

        override fun onDescriptorWrite(
            gatt: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int
        ) {
            when (status) {
                BluetoothGatt.GATT_SUCCESS -> {
                    Timber.d("Wrote to descriptor ${descriptor.uuid}")
                    BleJob.EnableNotification.resumeWithSuccess(Unit)
                }
                else -> {
                    BleJob.EnableNotification.resumeWithError("Descriptor write failed for ${descriptor.uuid}, error: $status")
                }
            }
        }

        @Deprecated("Deprecated for Android 13+",
            ReplaceWith("onCharacteristicChanged(gatt, characteristic, characteristic.value)")
        )
        @Suppress("DEPRECATION")
        override fun onCharacteristicChanged(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
        ) {
            onCharacteristicChanged(gatt, characteristic, characteristic.value)
        }

        override fun onCharacteristicChanged(
            gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic, value: ByteArray
        ) {
            Timber.d("Characteristic ${characteristic.uuid} changed | value: ${value.toHexString()}")
            // Find per-device listeners and notify
            deviceGattMap.values.first { it.gatt == gatt }.listeners.forEach { listener ->
                listener.get()?.onNotification?.run {
                    this(characteristic.uuid, value.toUByteArray())
                }
            }
            // Notify generic listeners
            genericListeners.forEach {
                it.get()?.onNotification?.run { this(characteristic.uuid, value.toUByteArray()) }
            }
        }
    }

    /**
     * Extensions
     */

    private fun BluetoothDevice.isConnected() = deviceGattMap.containsKey(this)

    /**
     * Public API
     */

    fun servicesOf(deviceAddress: String): Result<List<BluetoothGattService>> =
        gattFromAddress(deviceAddress)?.let { gatt ->
            Result.success(gatt.services.toList())
        } ?: Result.failure(Exception("No device found with address $deviceAddress"))

    // Register for device specific callbacks
    fun registerListener(deviceAddress: String, listener: BleEventListener): Result<Unit> {
        deviceFromAddress(deviceAddress)?.let { bleDevice ->
            deviceGattMap[bleDevice]?.let {
                it.listeners.add(WeakReference(listener))
                Result.success(Unit)
            }
        }
            ?: return Result.failure(Exception("No connected device found with address $deviceAddress"))
        // Clean up garbage collected listeners
        deviceGattMap.forEachValue(Long.MAX_VALUE) { entry ->
            entry.listeners = entry.listeners.filter { it.get() != null }.toMutableSet()
        }
        return Result.success(Unit)
    }

    // Register for all callbacks
    fun registerListener(listener: BleEventListener): Result<Unit> {
        genericListeners.add(WeakReference(listener))
        // Clean up garbage collected listeners
        genericListeners = genericListeners.filter { it.get() != null }.toMutableSet()
        return Result.success(Unit)
    }

    // Unregister from device-specific and generic callbacks
    fun unregisterListener(listener: BleEventListener) {
        // Generic listeners
        genericListeners =
            genericListeners.filter { (it.get() != null) && (it.get() != listener) }.toMutableSet()

        // Device Specific listeners
        deviceGattMap.forEachValue(Long.MAX_VALUE) { entry ->
            entry.listeners =
                entry.listeners.filter { (it.get() != null) && (it.get() != listener) }
                    .toMutableSet()
        }
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_SCAN")
    suspend fun startScan(
        filters: List<ScanFilter>, settings: ScanSettings? = ScanSettings.Builder().build()
    ): Result<MutableSharedFlow<ScanResult>> {
        val flow = MutableSharedFlow<ScanResult>()
        val id = flow.hashCode()
        val callback = scanCallbackFactory(flow)
        scanObserverMap[id] = callback
        scanner.startScan(filters, settings, callback)
        return Result.success(flow)
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_SCAN")
    suspend fun stopScan(observer: MutableSharedFlow<ScanResult>): Result<Unit> {
        val id = observer.hashCode()
        scanner.stopScan(scanObserverMap.getValue(id))
        return Result.success(Unit)
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    suspend fun connect(deviceAddress: String): Result<Unit> {
        val bleDevice = deviceFromAddress(deviceAddress)
            ?: return Result.failure(Exception("No scanned device found with address $deviceAddress"))

        // Check if we're already connected
        if (bleDevice.isConnected()) {
            Timber.i("$deviceAddress is already connected.")
            return Result.success(Unit)
        }

        var status = Result.success(Unit) // Assume success and update if failure
        BleJob.Connect.suspendWithTimeout(10000) {
            bleDevice.connectGatt(
                context, false, connectedCallback
            )
        }.onSuccess { deviceGattMap[bleDevice] = DeviceEntry(it) }
            .onFailure { status = Result.failure(it) }
        return status
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    suspend fun discoverCharacteristics(deviceAddress: String): Result<Unit> {
        val gatt = gattFromAddress(deviceAddress)
            ?: return Result.failure(Exception("No device found with address $deviceAddress"))

        return BleJob.DiscoverServices.suspendWithTimeout(10000) {
            if (!gatt.discoverServices()) {
                BleJob.DiscoverServices.resumeWithError("Failed to start service discovery")
            }
        }
    }

    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    suspend fun enableNotification(
        deviceAddress: String, characteristic: UUID
    ): Result<Unit> {
        Timber.d("Enabling notifications for $characteristic")
        val gatt = gattFromAddress(deviceAddress)
            ?: return Result.failure(Exception("No device found with address $deviceAddress"))
        val char = charFromUuid(gatt, characteristic)
            ?: return Result.failure(Exception("Characteristic $characteristic not found"))
        val payload = when {
            char.isIndicatable() -> BluetoothGattDescriptor.ENABLE_INDICATION_VALUE
            char.isNotifiable() -> BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            else -> return Result.failure(Exception("$characteristic doesn't support notifications/indications"))
        }
        // This method has no associated callback
        if (!gatt.setCharacteristicNotification(char, true)) {
            return Result.failure(
                Exception("setCharacteristicNotification failed for $characteristic")
            )
        }
        char.getDescriptor(CoreUUID.CCC_DESCRIPTOR.uuid)?.let { descriptor ->
            return BleJob.EnableNotification.suspendWithTimeout(10000) {
                if (!writeDescriptor(gatt, descriptor, payload)) {
                    BleJob.EnableNotification.resumeWithError("writeDescriptor failed for ${descriptor.uuid}")
                }
            }
        } ?: return Result.failure(Exception("Could not find descriptor for $characteristic"))
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    suspend fun readCharacteristic(
        deviceAddress: String, characteristic: UUID, timeout: Long = 5000
    ): Result<UByteArray> {
        val gatt = gattFromAddress(deviceAddress)
            ?: return Result.failure(Exception("No device found with address $deviceAddress"))
        val char = charFromUuid(gatt, characteristic)
            ?: return Result.failure(Exception("Characteristic $characteristic not found"))
        return BleJob.Read.suspendWithTimeout(timeout) {
            if (!gatt.readCharacteristic(char)) {
                BleJob.Read.resumeWithError("Read of $characteristic failed")
            }
        }
    }

    @OptIn(ExperimentalUnsignedTypes::class)
    @RequiresPermission(value = "android.permission.BLUETOOTH_CONNECT")
    suspend fun writeCharacteristic(
        deviceAddress: String, characteristic: UUID, payload: UByteArray
    ): Result<Unit> {
        val gatt = gattFromAddress(deviceAddress)
            ?: return Result.failure(Exception("No device found with address $deviceAddress"))
        val char = charFromUuid(gatt, characteristic)
            ?: return Result.failure(Exception("Characteristic $characteristic not found"))
        val writeType = when {
            char.isWritable() -> BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            char.isWritableWithoutResponse() -> {
                BluetoothGattCharacteristic.WRITE_TYPE_NO_RESPONSE
            }
            else -> {
                return Result.failure(Exception("Characteristic $characteristic cannot be written to"))
            }
        }
        return BleJob.Write.suspendWithTimeout(5000) {
            Timber.d("Writing characteristic $characteristic ==> ${payload.toHexString()}")
            if (!writeCharacteristic(gatt, char, payload.toByteArray(), writeType)) {
                BleJob.Write.resumeWithError("Write of $characteristic failed")
            }
        }
    }
}
