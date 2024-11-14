package network

import co.touchlab.kermit.Logger
import com.benasher44.uuid.Uuid
import com.juul.kable.Characteristic
import com.juul.kable.PlatformAdvertisement
import com.juul.kable.Scanner
import com.juul.kable.WriteType
import com.juul.kable.logs.Logging
import com.juul.kable.logs.SystemLogEngine
import com.juul.kable.peripheral
import domain.network.IBleApi
import entity.connector.GoProId
import entity.network.BleAdvertisement
import entity.network.BleDevice
import entity.network.BleNotification
import extensions.toPrettyHexString
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.merge
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.job
import kotlinx.coroutines.launch

internal class KableAdvertisement(val platformAdvertisement: PlatformAdvertisement) :
    BleAdvertisement {
    override val name = platformAdvertisement.name
    override val id = platformAdvertisement.identifier.toString()
}

private val logger = Logger.withTag("KableBle")

// TODO use Result for return values here.
@OptIn(ExperimentalUnsignedTypes::class)
private class KableDevice(
    adv: PlatformAdvertisement,
    dispatcher: CoroutineDispatcher
) : BleDevice {
    // Last 4 of serial number.
    override val id = adv.name?.let { GoProId(it.takeLast(4)) }
        ?: throw Exception("Can not create Kable device with an advertisement that does not contain a deviec name.")
    val notifications = MutableSharedFlow<BleNotification>()

    // TODO this has been fixed. Update Kable and rmeove.
    // Intermediary scope needed until https://github.com/JuulLabs/kable/issues/577 is resolved.
    private val peripheralScope = CoroutineScope(Job())
    private val scope =
        CoroutineScope(dispatcher + peripheralScope.coroutineContext + Job(peripheralScope.coroutineContext.job))
    val peripheral = scope.peripheral(adv) {
        logging {
            level = Logging.Level.Warnings // TODO this doesn't appear to be working.
        }
        onServicesDiscovered {
            // TODO this seems hacky. There must a better way.
            scope.launch {
                onServicesDiscoveredEvent.send(Unit)
            }
        }
    }
    private val onServicesDiscoveredEvent = Channel<Unit>()

    private fun characteristicFromUuid(uuid: Uuid): Characteristic? {
        // TODO this is extremely inefficient. Should do this once to create a map of UUID's to characteristics. We need to do this anyway to
        // translate to a services domain model
        peripheral.services?.let { services ->
            for (service in services) {
                try {
                    service.characteristics.first { it.characteristicUuid == uuid }
                        .let { return it }
                } catch (exc: NoSuchElementException) {
                    // The characteristic wasn't found in this service. Go to the next
                    continue
                }
            }
        } ?: run {
            logger.w("Services have not yet been discovered")
        }
        return null
    }

    // TODO We should timeout here.
    suspend fun connect() {
        logger.d("Establishing BLE connection to $id")
        peripheral.connect()
        logger.d("BLE connection established. Waiting for services to be discovered")
        onServicesDiscoveredEvent.receive()
        logger.d("Services discovered.")
    }


    @OptIn(ExperimentalUnsignedTypes::class)
    suspend fun enableNotifications(uuids: Set<Uuid>): Boolean {
        uuids.forEach { uuid ->
            characteristicFromUuid(uuid)?.let { characteristic ->
                logger.d("Enabling notifications for ${characteristic.characteristicUuid}")
                scope.launch {
                    peripheral.observe(characteristic).catch { exc ->
                        logger.e(exc.toString())
                    }.onEach {
                        logger.d("Received ${it.toPrettyHexString()} on ${characteristic.characteristicUuid}")
                    }.collect { data ->
                        // Forward to our observers.
                        notifications.emit(BleNotification(uuid, data.toUByteArray()))
                    }
                }
            } ?: run {
                logger.e("Could not find characteristic with uuid: $uuid")
                return false
            }
        }
        return true
    }

    suspend fun readCharacteristic(uuid: Uuid): UByteArray? =
        characteristicFromUuid(uuid)?.let { peripheral.read(it) }?.toUByteArray()

    suspend fun writeCharacteristic(uuid: Uuid, data: UByteArray): Boolean =
        characteristicFromUuid(uuid)?.let {
            peripheral.write(
                it,
                data.toByteArray(),
                WriteType.WithResponse
            )
        } != null


    suspend fun disconnect(): Boolean {
        peripheral.disconnect()
        scope.cancel() // TODO do we really want / need to do this here?
        return true // TODO how to wait for / check disconnection?
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal class KableBle(private val dispatcher: CoroutineDispatcher) : IBleApi {
    // Map domain objects to Kable specific objects
    private val deviceMap = mutableMapOf<GoProId, KableDevice>()
    private val nameAdvMap = mutableMapOf<String, KableAdvertisement>()

    override fun notificationsForConnection(device: BleDevice): Result<Flow<BleNotification>> =
        deviceMap[device.id]?.notifications?.let { Result.success(it) }
            ?: Result.failure(Exception("Could not find device"))

    override fun receiveDisconnects(): Flow<BleDevice> =
        deviceMap.values.map { device ->
            device.peripheral.state
                .filter { it is com.juul.kable.State.Disconnected }
                .map {
                    object : BleDevice {
                        override val id = device.id
                    }
                }
        }.merge()

    override fun scan(serviceUUIDs: Set<Uuid>?): Result<Flow<BleAdvertisement>> {
        val scanner = Scanner {
            filters {
                match {
                    serviceUUIDs?.let {
                        services = serviceUUIDs.toList()
                    }
                }
            }
            logging {
                engine = SystemLogEngine
                level = Logging.Level.Events
                format = Logging.Format.Multiline
            }
        }
        return Result.success(
            scanner.advertisements
                .onStart { nameAdvMap.clear() }
                .filter { it.name != null }
                .onEach {
                    logger.d("Received advertisement: ${it.identifier} ==> ${it.name!!}")
                    nameAdvMap[it.name!!] = KableAdvertisement(it)
                }
                .map { KableAdvertisement(it) }
        )
    }

    override suspend fun connect(advertisement: BleAdvertisement): Result<BleDevice> =
        nameAdvMap[advertisement.name]?.let { adv ->
            KableDevice(adv.platformAdvertisement, dispatcher)
        }?.let { device ->
            device.connect() // TODO how to wait for connect
            deviceMap[device.id] = device
            Result.success(device)
        } ?: Result.failure(Exception("advertisement ${advertisement.id} not found"))

    override suspend fun enableNotifications(
        device: BleDevice,
        uuids: Set<Uuid>
    ): Result<Unit> =
        deviceMap[device.id]?.enableNotifications(uuids)?.let { Result.success(Unit) }
            ?: Result.failure(
                Exception("connected $device does not exist")
            )

    override suspend fun readCharacteristic(device: BleDevice, uuid: Uuid): Result<UByteArray> =
        deviceMap[device.id]?.readCharacteristic(uuid)?.let { Result.success(it) }
            ?: Result.failure(
                Exception("connected $device does not exist")
            )

    override suspend fun writeCharacteristic(
        device: BleDevice,
        uuid: Uuid,
        data: UByteArray
    ): Result<Unit> =
        deviceMap[device.id]?.writeCharacteristic(uuid, data)?.let { Result.success(Unit) }
            ?: Result.failure(
                Exception("connected $device does not exist")
            )

    override suspend fun disconnect(device: BleDevice): Result<Unit> =
        deviceMap[device.id]?.disconnect()?.let { Result.success(Unit) }
            ?: Result.failure(
                Exception("connected $device does not exist")
            )
}