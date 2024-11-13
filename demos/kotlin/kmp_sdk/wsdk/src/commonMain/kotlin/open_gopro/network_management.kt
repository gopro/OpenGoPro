@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumProvisioning(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumProvisioning && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumProvisioning.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object PROVISIONING_UNKNOWN : EnumProvisioning(0, "PROVISIONING_UNKNOWN")
    public object PROVISIONING_NEVER_STARTED : EnumProvisioning(1, "PROVISIONING_NEVER_STARTED")
    public object PROVISIONING_STARTED : EnumProvisioning(2, "PROVISIONING_STARTED")
    public object PROVISIONING_ABORTED_BY_SYSTEM : EnumProvisioning(3, "PROVISIONING_ABORTED_BY_SYSTEM")
    public object PROVISIONING_CANCELLED_BY_USER : EnumProvisioning(4, "PROVISIONING_CANCELLED_BY_USER")
    public object PROVISIONING_SUCCESS_NEW_AP : EnumProvisioning(5, "PROVISIONING_SUCCESS_NEW_AP")
    public object PROVISIONING_SUCCESS_OLD_AP : EnumProvisioning(6, "PROVISIONING_SUCCESS_OLD_AP")
    public object PROVISIONING_ERROR_FAILED_TO_ASSOCIATE : EnumProvisioning(7, "PROVISIONING_ERROR_FAILED_TO_ASSOCIATE")
    public object PROVISIONING_ERROR_PASSWORD_AUTH : EnumProvisioning(8, "PROVISIONING_ERROR_PASSWORD_AUTH")
    public object PROVISIONING_ERROR_EULA_BLOCKING : EnumProvisioning(9, "PROVISIONING_ERROR_EULA_BLOCKING")
    public object PROVISIONING_ERROR_NO_INTERNET : EnumProvisioning(10, "PROVISIONING_ERROR_NO_INTERNET")
    public object PROVISIONING_ERROR_UNSUPPORTED_TYPE : EnumProvisioning(11, "PROVISIONING_ERROR_UNSUPPORTED_TYPE")
    public class UNRECOGNIZED(value: Int) : EnumProvisioning(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumProvisioning> {
        public val values: List<open_gopro.EnumProvisioning> by lazy { listOf(PROVISIONING_UNKNOWN, PROVISIONING_NEVER_STARTED, PROVISIONING_STARTED, PROVISIONING_ABORTED_BY_SYSTEM, PROVISIONING_CANCELLED_BY_USER, PROVISIONING_SUCCESS_NEW_AP, PROVISIONING_SUCCESS_OLD_AP, PROVISIONING_ERROR_FAILED_TO_ASSOCIATE, PROVISIONING_ERROR_PASSWORD_AUTH, PROVISIONING_ERROR_EULA_BLOCKING, PROVISIONING_ERROR_NO_INTERNET, PROVISIONING_ERROR_UNSUPPORTED_TYPE) }
        override fun fromValue(value: Int): open_gopro.EnumProvisioning = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumProvisioning = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumProvisioning with name: $name")
    }
}

@pbandk.Export
public sealed class EnumScanning(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumScanning && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumScanning.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object SCANNING_UNKNOWN : EnumScanning(0, "SCANNING_UNKNOWN")
    public object SCANNING_NEVER_STARTED : EnumScanning(1, "SCANNING_NEVER_STARTED")
    public object SCANNING_STARTED : EnumScanning(2, "SCANNING_STARTED")
    public object SCANNING_ABORTED_BY_SYSTEM : EnumScanning(3, "SCANNING_ABORTED_BY_SYSTEM")
    public object SCANNING_CANCELLED_BY_USER : EnumScanning(4, "SCANNING_CANCELLED_BY_USER")
    public object SCANNING_SUCCESS : EnumScanning(5, "SCANNING_SUCCESS")
    public class UNRECOGNIZED(value: Int) : EnumScanning(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumScanning> {
        public val values: List<open_gopro.EnumScanning> by lazy { listOf(SCANNING_UNKNOWN, SCANNING_NEVER_STARTED, SCANNING_STARTED, SCANNING_ABORTED_BY_SYSTEM, SCANNING_CANCELLED_BY_USER, SCANNING_SUCCESS) }
        override fun fromValue(value: Int): open_gopro.EnumScanning = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumScanning = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumScanning with name: $name")
    }
}

@pbandk.Export
public sealed class EnumScanEntryFlags(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumScanEntryFlags && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumScanEntryFlags.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object SCAN_FLAG_OPEN : EnumScanEntryFlags(0, "SCAN_FLAG_OPEN")
    public object SCAN_FLAG_AUTHENTICATED : EnumScanEntryFlags(1, "SCAN_FLAG_AUTHENTICATED")
    public object SCAN_FLAG_CONFIGURED : EnumScanEntryFlags(2, "SCAN_FLAG_CONFIGURED")
    public object SCAN_FLAG_BEST_SSID : EnumScanEntryFlags(4, "SCAN_FLAG_BEST_SSID")
    public object SCAN_FLAG_ASSOCIATED : EnumScanEntryFlags(8, "SCAN_FLAG_ASSOCIATED")
    public object SCAN_FLAG_UNSUPPORTED_TYPE : EnumScanEntryFlags(16, "SCAN_FLAG_UNSUPPORTED_TYPE")
    public class UNRECOGNIZED(value: Int) : EnumScanEntryFlags(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumScanEntryFlags> {
        public val values: List<open_gopro.EnumScanEntryFlags> by lazy { listOf(SCAN_FLAG_OPEN, SCAN_FLAG_AUTHENTICATED, SCAN_FLAG_CONFIGURED, SCAN_FLAG_BEST_SSID, SCAN_FLAG_ASSOCIATED, SCAN_FLAG_UNSUPPORTED_TYPE) }
        override fun fromValue(value: Int): open_gopro.EnumScanEntryFlags = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumScanEntryFlags = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumScanEntryFlags with name: $name")
    }
}

@pbandk.Export
public data class NotifProvisioningState(
    val provisioningState: open_gopro.EnumProvisioning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.NotifProvisioningState = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifProvisioningState> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.NotifProvisioningState> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.NotifProvisioningState = open_gopro.NotifProvisioningState.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifProvisioningState> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifProvisioningState",
            messageClass = open_gopro.NotifProvisioningState::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = open_gopro.NotifProvisioningState::provisioningState
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class NotifStartScanning(
    val scanningState: open_gopro.EnumScanning,
    val scanId: Int? = null,
    val totalEntries: Int? = null,
    val totalConfiguredSsid: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.NotifStartScanning = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifStartScanning> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.NotifStartScanning> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.NotifStartScanning = open_gopro.NotifStartScanning.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifStartScanning> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifStartScanning",
            messageClass = open_gopro.NotifStartScanning::class,
            messageCompanion = this,
            fields = buildList(4) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scanning_state",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumScanning.Companion, hasPresence = true),
                        jsonName = "scanningState",
                        value = open_gopro.NotifStartScanning::scanningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = open_gopro.NotifStartScanning::scanId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "total_entries",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "totalEntries",
                        value = open_gopro.NotifStartScanning::totalEntries
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "total_configured_ssid",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "totalConfiguredSsid",
                        value = open_gopro.NotifStartScanning::totalConfiguredSsid
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestConnect(
    val ssid: String,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestConnect = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestConnect> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestConnect> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestConnect = open_gopro.RequestConnect.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestConnect> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnect",
            messageClass = open_gopro.RequestConnect::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = open_gopro.RequestConnect::ssid
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestConnectNew(
    val ssid: String,
    val password: String,
    val staticIp: pbandk.ByteArr? = null,
    val gateway: pbandk.ByteArr? = null,
    val subnet: pbandk.ByteArr? = null,
    val dnsPrimary: pbandk.ByteArr? = null,
    val dnsSecondary: pbandk.ByteArr? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestConnectNew = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestConnectNew> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestConnectNew> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestConnectNew = open_gopro.RequestConnectNew.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestConnectNew> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnectNew",
            messageClass = open_gopro.RequestConnectNew::class,
            messageCompanion = this,
            fields = buildList(7) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = open_gopro.RequestConnectNew::ssid
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "password",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "password",
                        value = open_gopro.RequestConnectNew::password
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "static_ip",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "staticIp",
                        value = open_gopro.RequestConnectNew::staticIp
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "gateway",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "gateway",
                        value = open_gopro.RequestConnectNew::gateway
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "subnet",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "subnet",
                        value = open_gopro.RequestConnectNew::subnet
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "dns_primary",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "dnsPrimary",
                        value = open_gopro.RequestConnectNew::dnsPrimary
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "dns_secondary",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "dnsSecondary",
                        value = open_gopro.RequestConnectNew::dnsSecondary
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestGetApEntries(
    val startIndex: Int,
    val maxEntries: Int,
    val scanId: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestGetApEntries = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetApEntries> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestGetApEntries> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestGetApEntries = open_gopro.RequestGetApEntries.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetApEntries> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetApEntries",
            messageClass = open_gopro.RequestGetApEntries::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "start_index",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "startIndex",
                        value = open_gopro.RequestGetApEntries::startIndex
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "max_entries",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "maxEntries",
                        value = open_gopro.RequestGetApEntries::maxEntries
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = open_gopro.RequestGetApEntries::scanId
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestReleaseNetwork(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestReleaseNetwork = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestReleaseNetwork> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestReleaseNetwork> {
        public val defaultInstance: open_gopro.RequestReleaseNetwork by lazy { open_gopro.RequestReleaseNetwork() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestReleaseNetwork = open_gopro.RequestReleaseNetwork.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestReleaseNetwork> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestReleaseNetwork",
            messageClass = open_gopro.RequestReleaseNetwork::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
public data class RequestStartScan(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestStartScan = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestStartScan> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestStartScan> {
        public val defaultInstance: open_gopro.RequestStartScan by lazy { open_gopro.RequestStartScan() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestStartScan = open_gopro.RequestStartScan.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestStartScan> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestStartScan",
            messageClass = open_gopro.RequestStartScan::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
public data class ResponseConnect(
    val result: open_gopro.EnumResultGeneric,
    val provisioningState: open_gopro.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseConnect = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseConnect> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseConnect> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseConnect = open_gopro.ResponseConnect.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseConnect> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnect",
            messageClass = open_gopro.ResponseConnect::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseConnect::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = open_gopro.ResponseConnect::provisioningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "timeout_seconds",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "timeoutSeconds",
                        value = open_gopro.ResponseConnect::timeoutSeconds
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class ResponseConnectNew(
    val result: open_gopro.EnumResultGeneric,
    val provisioningState: open_gopro.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseConnectNew = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseConnectNew> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseConnectNew> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseConnectNew = open_gopro.ResponseConnectNew.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseConnectNew> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnectNew",
            messageClass = open_gopro.ResponseConnectNew::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseConnectNew::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "provisioning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumProvisioning.Companion, hasPresence = true),
                        jsonName = "provisioningState",
                        value = open_gopro.ResponseConnectNew::provisioningState
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "timeout_seconds",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "timeoutSeconds",
                        value = open_gopro.ResponseConnectNew::timeoutSeconds
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class ResponseGetApEntries(
    val result: open_gopro.EnumResultGeneric,
    val scanId: Int,
    val entries: List<open_gopro.ResponseGetApEntries.ScanEntry> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseGetApEntries = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGetApEntries> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseGetApEntries> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseGetApEntries = open_gopro.ResponseGetApEntries.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGetApEntries> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGetApEntries",
            messageClass = open_gopro.ResponseGetApEntries::class,
            messageCompanion = this,
            fields = buildList(3) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseGetApEntries::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scan_id",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "scanId",
                        value = open_gopro.ResponseGetApEntries::scanId
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "entries",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.ResponseGetApEntries.ScanEntry>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = open_gopro.ResponseGetApEntries.ScanEntry.Companion)),
                        jsonName = "entries",
                        value = open_gopro.ResponseGetApEntries::entries
                    )
                )
            }
        )
    }

    public data class ScanEntry(
        val ssid: String,
        val signalStrengthBars: Int,
        val signalFrequencyMhz: Int,
        val scanEntryFlags: Int,
        override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
    ) : pbandk.Message {
        override operator fun plus(other: pbandk.Message?): open_gopro.ResponseGetApEntries.ScanEntry = protoMergeImpl(other)
        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGetApEntries.ScanEntry> get() = Companion.descriptor
        override val protoSize: Int by lazy { super.protoSize }
        public companion object : pbandk.Message.Companion<open_gopro.ResponseGetApEntries.ScanEntry> {
            override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseGetApEntries.ScanEntry = open_gopro.ResponseGetApEntries.ScanEntry.decodeWithImpl(u)

            override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGetApEntries.ScanEntry> = pbandk.MessageDescriptor(
                fullName = "open_gopro.ResponseGetApEntries.ScanEntry",
                messageClass = open_gopro.ResponseGetApEntries.ScanEntry::class,
                messageCompanion = this,
                fields = buildList(4) {
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "ssid",
                            number = 1,
                            type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                            jsonName = "ssid",
                            value = open_gopro.ResponseGetApEntries.ScanEntry::ssid
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_strength_bars",
                            number = 2,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalStrengthBars",
                            value = open_gopro.ResponseGetApEntries.ScanEntry::signalStrengthBars
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_frequency_mhz",
                            number = 4,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalFrequencyMhz",
                            value = open_gopro.ResponseGetApEntries.ScanEntry::signalFrequencyMhz
                        )
                    )
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "scan_entry_flags",
                            number = 5,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "scanEntryFlags",
                            value = open_gopro.ResponseGetApEntries.ScanEntry::scanEntryFlags
                        )
                    )
                }
            )
        }
    }
}

@pbandk.Export
public data class ResponseStartScanning(
    val result: open_gopro.EnumResultGeneric,
    val scanningState: open_gopro.EnumScanning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseStartScanning = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseStartScanning> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseStartScanning> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseStartScanning = open_gopro.ResponseStartScanning.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseStartScanning> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseStartScanning",
            messageClass = open_gopro.ResponseStartScanning::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseStartScanning::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "scanning_state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumScanning.Companion, hasPresence = true),
                        jsonName = "scanningState",
                        value = open_gopro.ResponseStartScanning::scanningState
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
    var provisioningState: open_gopro.EnumProvisioning? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> provisioningState = _fieldValue as open_gopro.EnumProvisioning
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
    var scanningState: open_gopro.EnumScanning? = null
    var scanId: Int? = null
    var totalEntries: Int? = null
    var totalConfiguredSsid: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> scanningState = _fieldValue as open_gopro.EnumScanning
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
public fun RequestReleaseNetwork?.orDefault(): open_gopro.RequestReleaseNetwork = this ?: RequestReleaseNetwork.defaultInstance

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
public fun RequestStartScan?.orDefault(): open_gopro.RequestStartScan = this ?: RequestStartScan.defaultInstance

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
    var result: open_gopro.EnumResultGeneric? = null
    var provisioningState: open_gopro.EnumProvisioning? = null
    var timeoutSeconds: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> provisioningState = _fieldValue as open_gopro.EnumProvisioning
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
    var result: open_gopro.EnumResultGeneric? = null
    var provisioningState: open_gopro.EnumProvisioning? = null
    var timeoutSeconds: Int? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> provisioningState = _fieldValue as open_gopro.EnumProvisioning
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
    var result: open_gopro.EnumResultGeneric? = null
    var scanId: Int? = null
    var entries: pbandk.ListWithSize.Builder<open_gopro.ResponseGetApEntries.ScanEntry>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> scanId = _fieldValue as Int
            3 -> entries = (entries ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.ResponseGetApEntries.ScanEntry> }
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
    var result: open_gopro.EnumResultGeneric? = null
    var scanningState: open_gopro.EnumScanning? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> scanningState = _fieldValue as open_gopro.EnumScanning
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
