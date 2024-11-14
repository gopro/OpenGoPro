@file:OptIn(pbandk.PublicForGeneratedCode::class)

package entity.operation.proto

@pbandk.Export
internal sealed class EnumProvisioning(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is entity.operation.proto.EnumProvisioning && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumProvisioning.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object PROVISIONING_UNKNOWN : EnumProvisioning(0, "PROVISIONING_UNKNOWN")
    internal object PROVISIONING_NEVER_STARTED : EnumProvisioning(1, "PROVISIONING_NEVER_STARTED")
    internal object PROVISIONING_STARTED : EnumProvisioning(2, "PROVISIONING_STARTED")
    internal object PROVISIONING_ABORTED_BY_SYSTEM : EnumProvisioning(3, "PROVISIONING_ABORTED_BY_SYSTEM")
    internal object PROVISIONING_CANCELLED_BY_USER : EnumProvisioning(4, "PROVISIONING_CANCELLED_BY_USER")
    internal object PROVISIONING_SUCCESS_NEW_AP : EnumProvisioning(5, "PROVISIONING_SUCCESS_NEW_AP")
    internal object PROVISIONING_SUCCESS_OLD_AP : EnumProvisioning(6, "PROVISIONING_SUCCESS_OLD_AP")
    internal object PROVISIONING_ERROR_FAILED_TO_ASSOCIATE : EnumProvisioning(7, "PROVISIONING_ERROR_FAILED_TO_ASSOCIATE")
    internal object PROVISIONING_ERROR_PASSWORD_AUTH : EnumProvisioning(8, "PROVISIONING_ERROR_PASSWORD_AUTH")
    internal object PROVISIONING_ERROR_EULA_BLOCKING : EnumProvisioning(9, "PROVISIONING_ERROR_EULA_BLOCKING")
    internal object PROVISIONING_ERROR_NO_INTERNET : EnumProvisioning(10, "PROVISIONING_ERROR_NO_INTERNET")
    internal object PROVISIONING_ERROR_UNSUPPORTED_TYPE : EnumProvisioning(11, "PROVISIONING_ERROR_UNSUPPORTED_TYPE")
    internal class UNRECOGNIZED(value: Int) : EnumProvisioning(value)

    internal companion object : pbandk.Message.Enum.Companion<entity.operation.proto.EnumProvisioning> {
        internal val values: List<entity.operation.proto.EnumProvisioning> by lazy { listOf(PROVISIONING_UNKNOWN, PROVISIONING_NEVER_STARTED, PROVISIONING_STARTED, PROVISIONING_ABORTED_BY_SYSTEM, PROVISIONING_CANCELLED_BY_USER, PROVISIONING_SUCCESS_NEW_AP, PROVISIONING_SUCCESS_OLD_AP, PROVISIONING_ERROR_FAILED_TO_ASSOCIATE, PROVISIONING_ERROR_PASSWORD_AUTH, PROVISIONING_ERROR_EULA_BLOCKING, PROVISIONING_ERROR_NO_INTERNET, PROVISIONING_ERROR_UNSUPPORTED_TYPE) }
        override fun fromValue(value: Int): entity.operation.proto.EnumProvisioning = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): entity.operation.proto.EnumProvisioning = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumProvisioning with name: $name")
    }
}

@pbandk.Export
internal sealed class EnumScanning(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is entity.operation.proto.EnumScanning && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumScanning.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object SCANNING_UNKNOWN : EnumScanning(0, "SCANNING_UNKNOWN")
    internal object SCANNING_NEVER_STARTED : EnumScanning(1, "SCANNING_NEVER_STARTED")
    internal object SCANNING_STARTED : EnumScanning(2, "SCANNING_STARTED")
    internal object SCANNING_ABORTED_BY_SYSTEM : EnumScanning(3, "SCANNING_ABORTED_BY_SYSTEM")
    internal object SCANNING_CANCELLED_BY_USER : EnumScanning(4, "SCANNING_CANCELLED_BY_USER")
    internal object SCANNING_SUCCESS : EnumScanning(5, "SCANNING_SUCCESS")
    internal class UNRECOGNIZED(value: Int) : EnumScanning(value)

    internal companion object : pbandk.Message.Enum.Companion<entity.operation.proto.EnumScanning> {
        internal val values: List<entity.operation.proto.EnumScanning> by lazy { listOf(SCANNING_UNKNOWN, SCANNING_NEVER_STARTED, SCANNING_STARTED, SCANNING_ABORTED_BY_SYSTEM, SCANNING_CANCELLED_BY_USER, SCANNING_SUCCESS) }
        override fun fromValue(value: Int): entity.operation.proto.EnumScanning = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): entity.operation.proto.EnumScanning = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumScanning with name: $name")
    }
}

@pbandk.Export
internal sealed class EnumScanEntryFlags(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is entity.operation.proto.EnumScanEntryFlags && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumScanEntryFlags.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object SCAN_FLAG_OPEN : EnumScanEntryFlags(0, "SCAN_FLAG_OPEN")
    internal object SCAN_FLAG_AUTHENTICATED : EnumScanEntryFlags(1, "SCAN_FLAG_AUTHENTICATED")
    internal object SCAN_FLAG_CONFIGURED : EnumScanEntryFlags(2, "SCAN_FLAG_CONFIGURED")
    internal object SCAN_FLAG_BEST_SSID : EnumScanEntryFlags(4, "SCAN_FLAG_BEST_SSID")
    internal object SCAN_FLAG_ASSOCIATED : EnumScanEntryFlags(8, "SCAN_FLAG_ASSOCIATED")
    internal object SCAN_FLAG_UNSUPPORTED_TYPE : EnumScanEntryFlags(16, "SCAN_FLAG_UNSUPPORTED_TYPE")
    internal class UNRECOGNIZED(value: Int) : EnumScanEntryFlags(value)

    internal companion object : pbandk.Message.Enum.Companion<entity.operation.proto.EnumScanEntryFlags> {
        internal val values: List<entity.operation.proto.EnumScanEntryFlags> by lazy { listOf(SCAN_FLAG_OPEN, SCAN_FLAG_AUTHENTICATED, SCAN_FLAG_CONFIGURED, SCAN_FLAG_BEST_SSID, SCAN_FLAG_ASSOCIATED, SCAN_FLAG_UNSUPPORTED_TYPE) }
        override fun fromValue(value: Int): entity.operation.proto.EnumScanEntryFlags = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): entity.operation.proto.EnumScanEntryFlags = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumScanEntryFlags with name: $name")
    }
}

@pbandk.Export
internal data class NotifProvisioningState(
    val provisioningState: entity.operation.proto.EnumProvisioning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.NotifProvisioningState = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.NotifProvisioningState> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.NotifProvisioningState> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.NotifProvisioningState = entity.operation.proto.NotifProvisioningState.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.NotifProvisioningState> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifProvisioningState",
            messageClass = entity.operation.proto.NotifProvisioningState::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = entity.operation.proto.NotifProvisioningState::provisioningState
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class NotifStartScanning(
    val scanningState: entity.operation.proto.EnumScanning,
    val scanId: Int? = null,
    val totalEntries: Int? = null,
    val totalConfiguredSsid: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.NotifStartScanning = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.NotifStartScanning> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.NotifStartScanning> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.NotifStartScanning = entity.operation.proto.NotifStartScanning.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.NotifStartScanning> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifStartScanning",
            messageClass = entity.operation.proto.NotifStartScanning::class,
            messageCompanion = this,
            fields = buildList(4) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scanning_state",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumScanning.Companion, hasPresence = true),
                        jsonName = "scanningState",
                        value = entity.operation.proto.NotifStartScanning::scanningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = entity.operation.proto.NotifStartScanning::scanId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "total_entries",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "totalEntries",
                        value = entity.operation.proto.NotifStartScanning::totalEntries
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "total_configured_ssid",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "totalConfiguredSsid",
                        value = entity.operation.proto.NotifStartScanning::totalConfiguredSsid
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestConnect(
    val ssid: String,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestConnect = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestConnect> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestConnect> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestConnect = entity.operation.proto.RequestConnect.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestConnect> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnect",
            messageClass = entity.operation.proto.RequestConnect::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = entity.operation.proto.RequestConnect::ssid
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestConnectNew(
    val ssid: String,
    val password: String,
    val staticIp: pbandk.ByteArr? = null,
    val gateway: pbandk.ByteArr? = null,
    val subnet: pbandk.ByteArr? = null,
    val dnsPrimary: pbandk.ByteArr? = null,
    val dnsSecondary: pbandk.ByteArr? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestConnectNew = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestConnectNew> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestConnectNew> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestConnectNew = entity.operation.proto.RequestConnectNew.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestConnectNew> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnectNew",
            messageClass = entity.operation.proto.RequestConnectNew::class,
            messageCompanion = this,
            fields = buildList(7) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = entity.operation.proto.RequestConnectNew::ssid
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "password",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "password",
                        value = entity.operation.proto.RequestConnectNew::password
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "static_ip",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "staticIp",
                        value = entity.operation.proto.RequestConnectNew::staticIp
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "gateway",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "gateway",
                        value = entity.operation.proto.RequestConnectNew::gateway
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "subnet",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "subnet",
                        value = entity.operation.proto.RequestConnectNew::subnet
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "dns_primary",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "dnsPrimary",
                        value = entity.operation.proto.RequestConnectNew::dnsPrimary
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "dns_secondary",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "dnsSecondary",
                        value = entity.operation.proto.RequestConnectNew::dnsSecondary
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestGetApEntries(
    val startIndex: Int,
    val maxEntries: Int,
    val scanId: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestGetApEntries = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestGetApEntries> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestGetApEntries> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestGetApEntries = entity.operation.proto.RequestGetApEntries.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestGetApEntries> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetApEntries",
            messageClass = entity.operation.proto.RequestGetApEntries::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "start_index",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "startIndex",
                        value = entity.operation.proto.RequestGetApEntries::startIndex
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "max_entries",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "maxEntries",
                        value = entity.operation.proto.RequestGetApEntries::maxEntries
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = entity.operation.proto.RequestGetApEntries::scanId
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestReleaseNetwork(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestReleaseNetwork = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestReleaseNetwork> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestReleaseNetwork> {
        internal val defaultInstance: entity.operation.proto.RequestReleaseNetwork by lazy { entity.operation.proto.RequestReleaseNetwork() }
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestReleaseNetwork = entity.operation.proto.RequestReleaseNetwork.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestReleaseNetwork> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestReleaseNetwork",
            messageClass = entity.operation.proto.RequestReleaseNetwork::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
internal data class RequestStartScan(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestStartScan = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestStartScan> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestStartScan> {
        internal val defaultInstance: entity.operation.proto.RequestStartScan by lazy { entity.operation.proto.RequestStartScan() }
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestStartScan = entity.operation.proto.RequestStartScan.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestStartScan> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestStartScan",
            messageClass = entity.operation.proto.RequestStartScan::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
internal data class ResponseConnect(
    val result: entity.operation.proto.EnumResultGeneric,
    val provisioningState: entity.operation.proto.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseConnect = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseConnect> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseConnect> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseConnect = entity.operation.proto.ResponseConnect.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseConnect> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnect",
            messageClass = entity.operation.proto.ResponseConnect::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = entity.operation.proto.ResponseConnect::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = entity.operation.proto.ResponseConnect::provisioningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "timeout_seconds",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "timeoutSeconds",
                        value = entity.operation.proto.ResponseConnect::timeoutSeconds
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class ResponseConnectNew(
    val result: entity.operation.proto.EnumResultGeneric,
    val provisioningState: entity.operation.proto.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseConnectNew = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseConnectNew> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseConnectNew> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseConnectNew = entity.operation.proto.ResponseConnectNew.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseConnectNew> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnectNew",
            messageClass = entity.operation.proto.ResponseConnectNew::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = entity.operation.proto.ResponseConnectNew::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = entity.operation.proto.ResponseConnectNew::provisioningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "timeout_seconds",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "timeoutSeconds",
                        value = entity.operation.proto.ResponseConnectNew::timeoutSeconds
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class ResponseGetApEntries(
    val result: entity.operation.proto.EnumResultGeneric,
    val scanId: Int,
    val entries: List<entity.operation.proto.ResponseGetApEntries.ScanEntry> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseGetApEntries = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseGetApEntries> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseGetApEntries> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseGetApEntries = entity.operation.proto.ResponseGetApEntries.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseGetApEntries> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGetApEntries",
            messageClass = entity.operation.proto.ResponseGetApEntries::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = entity.operation.proto.ResponseGetApEntries::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = entity.operation.proto.ResponseGetApEntries::scanId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "entries",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Repeated<entity.operation.proto.ResponseGetApEntries.ScanEntry>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = entity.operation.proto.ResponseGetApEntries.ScanEntry.Companion)),
                        jsonName = "entries",
                        value = entity.operation.proto.ResponseGetApEntries::entries
                    )
                )
            }
        )
    }

    internal data class ScanEntry(
        val ssid: String,
        val signalStrengthBars: Int,
        val signalFrequencyMhz: Int,
        val scanEntryFlags: Int,
        override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
    ) : pbandk.Message {
        override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseGetApEntries.ScanEntry = protoMergeImpl(other)
        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseGetApEntries.ScanEntry> get() = Companion.descriptor
        override val protoSize: Int by lazy { super.protoSize }
        internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseGetApEntries.ScanEntry> {
            override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseGetApEntries.ScanEntry = entity.operation.proto.ResponseGetApEntries.ScanEntry.decodeWithImpl(u)

            override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseGetApEntries.ScanEntry> = pbandk.MessageDescriptor(
                fullName = "open_gopro.ResponseGetApEntries.ScanEntry",
                messageClass = entity.operation.proto.ResponseGetApEntries.ScanEntry::class,
                messageCompanion = this,
                fields = buildList(4) {
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "ssid",
                            number = 1,
                            type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                            jsonName = "ssid",
                            value = entity.operation.proto.ResponseGetApEntries.ScanEntry::ssid
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_strength_bars",
                            number = 2,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalStrengthBars",
                            value = entity.operation.proto.ResponseGetApEntries.ScanEntry::signalStrengthBars
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_frequency_mhz",
                            number = 4,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalFrequencyMhz",
                            value = entity.operation.proto.ResponseGetApEntries.ScanEntry::signalFrequencyMhz
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "scan_entry_flags",
                            number = 5,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "scanEntryFlags",
                            value = entity.operation.proto.ResponseGetApEntries.ScanEntry::scanEntryFlags
                        )
                    )
                }
            )
        }
    }
}

@pbandk.Export
internal data class ResponseStartScanning(
    val result: entity.operation.proto.EnumResultGeneric,
    val scanningState: entity.operation.proto.EnumScanning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseStartScanning = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseStartScanning> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseStartScanning> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseStartScanning = entity.operation.proto.ResponseStartScanning.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseStartScanning> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseStartScanning",
            messageClass = entity.operation.proto.ResponseStartScanning::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = entity.operation.proto.ResponseStartScanning::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scanning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumScanning.Companion, hasPresence = true),
                        jsonName = "scanningState",
                        value = entity.operation.proto.ResponseStartScanning::scanningState
                    )
                )
            }
        )
    }
}

private fun NotifProvisioningState.protoMergeImpl(plus: pbandk.Message?): NotifProvisioningState = (plus as? NotifProvisioningState)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifProvisioningState.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifProvisioningState {
    var provisioningState: entity.operation.proto.EnumProvisioning? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> provisioningState = _fieldValue as entity.operation.proto.EnumProvisioning
        }
    }

    if (provisioningState == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
    }
    return NotifProvisioningState(provisioningState!!, unknownFields)
}

private fun NotifStartScanning.protoMergeImpl(plus: pbandk.Message?): NotifStartScanning = (plus as? NotifStartScanning)?.let {
    it.copy(
        scanId = plus.scanId ?: scanId,
        totalEntries = plus.totalEntries ?: totalEntries,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifStartScanning.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifStartScanning {
    var scanningState: entity.operation.proto.EnumScanning? = null
    var scanId: Int? = null
    var totalEntries: Int? = null
    var totalConfiguredSsid: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> scanningState = _fieldValue as entity.operation.proto.EnumScanning
            2 -> scanId = _fieldValue as Int
            3 -> totalEntries = _fieldValue as Int
            4 -> totalConfiguredSsid = _fieldValue as Int
        }
    }

    if (scanningState == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("scanning_state")
    }
    if (totalConfiguredSsid == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("total_configured_ssid")
    }
    return NotifStartScanning(scanningState!!, scanId, totalEntries, totalConfiguredSsid!!, unknownFields)
}

private fun RequestConnect.protoMergeImpl(plus: pbandk.Message?): RequestConnect = (plus as? RequestConnect)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestConnect.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestConnect {
    var ssid: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> ssid = _fieldValue as String
        }
    }

    if (ssid == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
    }
    return RequestConnect(ssid!!, unknownFields)
}

private fun RequestConnectNew.protoMergeImpl(plus: pbandk.Message?): RequestConnectNew = (plus as? RequestConnectNew)?.let {
    it.copy(
        staticIp = plus.staticIp ?: staticIp,
        gateway = plus.gateway ?: gateway,
        subnet = plus.subnet ?: subnet,
        dnsPrimary = plus.dnsPrimary ?: dnsPrimary,
        dnsSecondary = plus.dnsSecondary ?: dnsSecondary,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestConnectNew.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestConnectNew {
    var ssid: String? = null
    var password: String? = null
    var staticIp: pbandk.ByteArr? = null
    var gateway: pbandk.ByteArr? = null
    var subnet: pbandk.ByteArr? = null
    var dnsPrimary: pbandk.ByteArr? = null
    var dnsSecondary: pbandk.ByteArr? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> ssid = _fieldValue as String
            2 -> password = _fieldValue as String
            3 -> staticIp = _fieldValue as pbandk.ByteArr
            4 -> gateway = _fieldValue as pbandk.ByteArr
            5 -> subnet = _fieldValue as pbandk.ByteArr
            6 -> dnsPrimary = _fieldValue as pbandk.ByteArr
            7 -> dnsSecondary = _fieldValue as pbandk.ByteArr
        }
    }

    if (ssid == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
    }
    if (password == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("password")
    }
    return RequestConnectNew(ssid!!, password!!, staticIp, gateway,
        subnet, dnsPrimary, dnsSecondary, unknownFields)
}

private fun RequestGetApEntries.protoMergeImpl(plus: pbandk.Message?): RequestGetApEntries = (plus as? RequestGetApEntries)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetApEntries.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetApEntries {
    var startIndex: Int? = null
    var maxEntries: Int? = null
    var scanId: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> startIndex = _fieldValue as Int
            2 -> maxEntries = _fieldValue as Int
            3 -> scanId = _fieldValue as Int
        }
    }

    if (startIndex == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("start_index")
    }
    if (maxEntries == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("max_entries")
    }
    if (scanId == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_id")
    }
    return RequestGetApEntries(startIndex!!, maxEntries!!, scanId!!, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestReleaseNetwork")
internal fun RequestReleaseNetwork?.orDefault(): entity.operation.proto.RequestReleaseNetwork = this ?: RequestReleaseNetwork.defaultInstance

private fun RequestReleaseNetwork.protoMergeImpl(plus: pbandk.Message?): RequestReleaseNetwork = (plus as? RequestReleaseNetwork)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestReleaseNetwork.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestReleaseNetwork {

    val unknownFields = u.readMessage(this) { _, _ -> }

    return RequestReleaseNetwork(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestStartScan")
internal fun RequestStartScan?.orDefault(): entity.operation.proto.RequestStartScan = this ?: RequestStartScan.defaultInstance

private fun RequestStartScan.protoMergeImpl(plus: pbandk.Message?): RequestStartScan = (plus as? RequestStartScan)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestStartScan.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestStartScan {

    val unknownFields = u.readMessage(this) { _, _ -> }

    return RequestStartScan(unknownFields)
}

private fun ResponseConnect.protoMergeImpl(plus: pbandk.Message?): ResponseConnect = (plus as? ResponseConnect)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseConnect.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseConnect {
    var result: entity.operation.proto.EnumResultGeneric? = null
    var provisioningState: entity.operation.proto.EnumProvisioning? = null
    var timeoutSeconds: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as entity.operation.proto.EnumResultGeneric
            2 -> provisioningState = _fieldValue as entity.operation.proto.EnumProvisioning
            3 -> timeoutSeconds = _fieldValue as Int
        }
    }

    if (result == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
    }
    if (provisioningState == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
    }
    if (timeoutSeconds == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("timeout_seconds")
    }
    return ResponseConnect(result!!, provisioningState!!, timeoutSeconds!!, unknownFields)
}

private fun ResponseConnectNew.protoMergeImpl(plus: pbandk.Message?): ResponseConnectNew = (plus as? ResponseConnectNew)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseConnectNew.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseConnectNew {
    var result: entity.operation.proto.EnumResultGeneric? = null
    var provisioningState: entity.operation.proto.EnumProvisioning? = null
    var timeoutSeconds: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as entity.operation.proto.EnumResultGeneric
            2 -> provisioningState = _fieldValue as entity.operation.proto.EnumProvisioning
            3 -> timeoutSeconds = _fieldValue as Int
        }
    }

    if (result == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
    }
    if (provisioningState == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
    }
    if (timeoutSeconds == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("timeout_seconds")
    }
    return ResponseConnectNew(result!!, provisioningState!!, timeoutSeconds!!, unknownFields)
}

private fun ResponseGetApEntries.protoMergeImpl(plus: pbandk.Message?): ResponseGetApEntries = (plus as? ResponseGetApEntries)?.let {
    it.copy(
        entries = entries + plus.entries,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGetApEntries.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseGetApEntries {
    var result: entity.operation.proto.EnumResultGeneric? = null
    var scanId: Int? = null
    var entries: pbandk.ListWithSize.Builder<entity.operation.proto.ResponseGetApEntries.ScanEntry>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as entity.operation.proto.EnumResultGeneric
            2 -> scanId = _fieldValue as Int
            3 -> entries = (entries ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<entity.operation.proto.ResponseGetApEntries.ScanEntry> }
        }
    }

    if (result == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
    }
    if (scanId == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_id")
    }
    return ResponseGetApEntries(result!!, scanId!!, pbandk.ListWithSize.Builder.fixed(entries), unknownFields)
}

private fun ResponseGetApEntries.ScanEntry.protoMergeImpl(plus: pbandk.Message?): ResponseGetApEntries.ScanEntry = (plus as? ResponseGetApEntries.ScanEntry)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGetApEntries.ScanEntry.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseGetApEntries.ScanEntry {
    var ssid: String? = null
    var signalStrengthBars: Int? = null
    var signalFrequencyMhz: Int? = null
    var scanEntryFlags: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> ssid = _fieldValue as String
            2 -> signalStrengthBars = _fieldValue as Int
            4 -> signalFrequencyMhz = _fieldValue as Int
            5 -> scanEntryFlags = _fieldValue as Int
        }
    }

    if (ssid == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
    }
    if (signalStrengthBars == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("signal_strength_bars")
    }
    if (signalFrequencyMhz == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("signal_frequency_mhz")
    }
    if (scanEntryFlags == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_entry_flags")
    }
    return ResponseGetApEntries.ScanEntry(ssid!!, signalStrengthBars!!, signalFrequencyMhz!!, scanEntryFlags!!, unknownFields)
}

private fun ResponseStartScanning.protoMergeImpl(plus: pbandk.Message?): ResponseStartScanning = (plus as? ResponseStartScanning)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseStartScanning.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseStartScanning {
    var result: entity.operation.proto.EnumResultGeneric? = null
    var scanningState: entity.operation.proto.EnumScanning? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as entity.operation.proto.EnumResultGeneric
            2 -> scanningState = _fieldValue as entity.operation.proto.EnumScanning
        }
    }

    if (result == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
    }
    if (scanningState == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("scanning_state")
    }
    return ResponseStartScanning(result!!, scanningState!!, unknownFields)
}
