@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumCOHNStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumCOHNStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCOHNStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object COHN_UNPROVISIONED : EnumCOHNStatus(0, "COHN_UNPROVISIONED")
    public object COHN_PROVISIONED : EnumCOHNStatus(1, "COHN_PROVISIONED")
    public class UNRECOGNIZED(value: Int) : EnumCOHNStatus(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumCOHNStatus> {
        public val values: List<open_gopro.EnumCOHNStatus> by lazy { listOf(COHN_UNPROVISIONED, COHN_PROVISIONED) }
        override fun fromValue(value: Int): open_gopro.EnumCOHNStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumCOHNStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCOHNStatus with name: $name")
    }
}

@pbandk.Export
public sealed class EnumCOHNNetworkState(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumCOHNNetworkState && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCOHNNetworkState.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object COHN_STATE_INIT : EnumCOHNNetworkState(0, "COHN_STATE_Init")
    public object COHN_STATE_ERROR : EnumCOHNNetworkState(1, "COHN_STATE_Error")
    public object COHN_STATE_EXIT : EnumCOHNNetworkState(2, "COHN_STATE_Exit")
    public object COHN_STATE_IDLE : EnumCOHNNetworkState(5, "COHN_STATE_Idle")
    public object COHN_STATE_NETWORK_CONNECTED : EnumCOHNNetworkState(27, "COHN_STATE_NetworkConnected")
    public object COHN_STATE_NETWORK_DISCONNECTED : EnumCOHNNetworkState(28, "COHN_STATE_NetworkDisconnected")
    public object COHN_STATE_CONNECTING_TO_NETWORK : EnumCOHNNetworkState(29, "COHN_STATE_ConnectingToNetwork")
    public object COHN_STATE_INVALID : EnumCOHNNetworkState(30, "COHN_STATE_Invalid")
    public class UNRECOGNIZED(value: Int) : EnumCOHNNetworkState(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumCOHNNetworkState> {
        public val values: List<open_gopro.EnumCOHNNetworkState> by lazy { listOf(COHN_STATE_INIT, COHN_STATE_ERROR, COHN_STATE_EXIT, COHN_STATE_IDLE, COHN_STATE_NETWORK_CONNECTED, COHN_STATE_NETWORK_DISCONNECTED, COHN_STATE_CONNECTING_TO_NETWORK, COHN_STATE_INVALID) }
        override fun fromValue(value: Int): open_gopro.EnumCOHNNetworkState = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumCOHNNetworkState = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCOHNNetworkState with name: $name")
    }
}

@pbandk.Export
public data class RequestGetCOHNStatus(
    val registerCohnStatus: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestGetCOHNStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetCOHNStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestGetCOHNStatus> {
        public val defaultInstance: open_gopro.RequestGetCOHNStatus by lazy { open_gopro.RequestGetCOHNStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestGetCOHNStatus = open_gopro.RequestGetCOHNStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetCOHNStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetCOHNStatus",
            messageClass = open_gopro.RequestGetCOHNStatus::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "register_cohn_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "registerCohnStatus",
                        value = open_gopro.RequestGetCOHNStatus::registerCohnStatus
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class NotifyCOHNStatus(
    val status: open_gopro.EnumCOHNStatus? = null,
    val state: open_gopro.EnumCOHNNetworkState? = null,
    val username: String? = null,
    val password: String? = null,
    val ipaddress: String? = null,
    val enabled: Boolean? = null,
    val ssid: String? = null,
    val macaddress: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.NotifyCOHNStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyCOHNStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.NotifyCOHNStatus> {
        public val defaultInstance: open_gopro.NotifyCOHNStatus by lazy { open_gopro.NotifyCOHNStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.NotifyCOHNStatus = open_gopro.NotifyCOHNStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyCOHNStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyCOHNStatus",
            messageClass = open_gopro.NotifyCOHNStatus::class,
            messageCompanion = this,
            fields = buildList(8) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumCOHNStatus.Companion, hasPresence = true),
                        jsonName = "status",
                        value = open_gopro.NotifyCOHNStatus::status
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumCOHNNetworkState.Companion, hasPresence = true),
                        jsonName = "state",
                        value = open_gopro.NotifyCOHNStatus::state
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "username",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "username",
                        value = open_gopro.NotifyCOHNStatus::username
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "password",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "password",
                        value = open_gopro.NotifyCOHNStatus::password
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ipaddress",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ipaddress",
                        value = open_gopro.NotifyCOHNStatus::ipaddress
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "enabled",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "enabled",
                        value = open_gopro.NotifyCOHNStatus::enabled
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = open_gopro.NotifyCOHNStatus::ssid
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "macaddress",
                        number = 8,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "macaddress",
                        value = open_gopro.NotifyCOHNStatus::macaddress
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestCreateCOHNCert(
    val override: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestCreateCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCreateCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestCreateCOHNCert> {
        public val defaultInstance: open_gopro.RequestCreateCOHNCert by lazy { open_gopro.RequestCreateCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestCreateCOHNCert = open_gopro.RequestCreateCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCreateCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCreateCOHNCert",
            messageClass = open_gopro.RequestCreateCOHNCert::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "override",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "override",
                        value = open_gopro.RequestCreateCOHNCert::override
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestClearCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestClearCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestClearCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestClearCOHNCert> {
        public val defaultInstance: open_gopro.RequestClearCOHNCert by lazy { open_gopro.RequestClearCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestClearCOHNCert = open_gopro.RequestClearCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestClearCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestClearCOHNCert",
            messageClass = open_gopro.RequestClearCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
public data class RequestCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestCOHNCert> {
        public val defaultInstance: open_gopro.RequestCOHNCert by lazy { open_gopro.RequestCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestCOHNCert = open_gopro.RequestCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCOHNCert",
            messageClass = open_gopro.RequestCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
public data class ResponseCOHNCert(
    val result: open_gopro.EnumResultGeneric? = null,
    val cert: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseCOHNCert> {
        public val defaultInstance: open_gopro.ResponseCOHNCert by lazy { open_gopro.ResponseCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseCOHNCert = open_gopro.ResponseCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseCOHNCert",
            messageClass = open_gopro.ResponseCOHNCert::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseCOHNCert::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "cert",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "cert",
                        value = open_gopro.ResponseCOHNCert::cert
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestSetCOHNSetting(
    val cohnActive: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestSetCOHNSetting = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetCOHNSetting> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestSetCOHNSetting> {
        public val defaultInstance: open_gopro.RequestSetCOHNSetting by lazy { open_gopro.RequestSetCOHNSetting() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestSetCOHNSetting = open_gopro.RequestSetCOHNSetting.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetCOHNSetting> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCOHNSetting",
            messageClass = open_gopro.RequestSetCOHNSetting::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "cohn_active",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "cohnActive",
                        value = open_gopro.RequestSetCOHNSetting::cohnActive
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetCOHNStatus")
public fun RequestGetCOHNStatus?.orDefault(): open_gopro.RequestGetCOHNStatus = this ?: RequestGetCOHNStatus.defaultInstance

private fun RequestGetCOHNStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetCOHNStatus = (plus as? RequestGetCOHNStatus)?.let {
    it.copy(
        registerCohnStatus = plus.registerCohnStatus ?: registerCohnStatus,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetCOHNStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetCOHNStatus {
    var registerCohnStatus: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> registerCohnStatus = _fieldValue as Boolean
        }
    }

    return RequestGetCOHNStatus(registerCohnStatus, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyCOHNStatus")
public fun NotifyCOHNStatus?.orDefault(): open_gopro.NotifyCOHNStatus = this ?: NotifyCOHNStatus.defaultInstance

private fun NotifyCOHNStatus.protoMergeImpl(plus: pbandk.Message?): NotifyCOHNStatus = (plus as? NotifyCOHNStatus)?.let {
    it.copy(
        status = plus.status ?: status,
        state = plus.state ?: state,
        username = plus.username ?: username,
        password = plus.password ?: password,
        ipaddress = plus.ipaddress ?: ipaddress,
        enabled = plus.enabled ?: enabled,
        ssid = plus.ssid ?: ssid,
        macaddress = plus.macaddress ?: macaddress,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyCOHNStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifyCOHNStatus {
    var status: open_gopro.EnumCOHNStatus? = null
    var state: open_gopro.EnumCOHNNetworkState? = null
    var username: String? = null
    var password: String? = null
    var ipaddress: String? = null
    var enabled: Boolean? = null
    var ssid: String? = null
    var macaddress: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> status = _fieldValue as open_gopro.EnumCOHNStatus
            2 -> state = _fieldValue as open_gopro.EnumCOHNNetworkState
            3 -> username = _fieldValue as String
            4 -> password = _fieldValue as String
            5 -> ipaddress = _fieldValue as String
            6 -> enabled = _fieldValue as Boolean
            7 -> ssid = _fieldValue as String
            8 -> macaddress = _fieldValue as String
        }
    }

    return NotifyCOHNStatus(status, state, username, password,
        ipaddress, enabled, ssid, macaddress, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCreateCOHNCert")
public fun RequestCreateCOHNCert?.orDefault(): open_gopro.RequestCreateCOHNCert = this ?: RequestCreateCOHNCert.defaultInstance

private fun RequestCreateCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestCreateCOHNCert = (plus as? RequestCreateCOHNCert)?.let {
    it.copy(
        override = plus.override ?: override,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCreateCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestCreateCOHNCert {
    var override: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> override = _fieldValue as Boolean
        }
    }

    return RequestCreateCOHNCert(override, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestClearCOHNCert")
public fun RequestClearCOHNCert?.orDefault(): open_gopro.RequestClearCOHNCert = this ?: RequestClearCOHNCert.defaultInstance

private fun RequestClearCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestClearCOHNCert = (plus as? RequestClearCOHNCert)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestClearCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestClearCOHNCert {

    val unknownFields = u.readMessage(this) { _, _ -> }

    return RequestClearCOHNCert(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCOHNCert")
public fun RequestCOHNCert?.orDefault(): open_gopro.RequestCOHNCert = this ?: RequestCOHNCert.defaultInstance

private fun RequestCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestCOHNCert = (plus as? RequestCOHNCert)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestCOHNCert {

    val unknownFields = u.readMessage(this) { _, _ -> }

    return RequestCOHNCert(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForResponseCOHNCert")
public fun ResponseCOHNCert?.orDefault(): open_gopro.ResponseCOHNCert = this ?: ResponseCOHNCert.defaultInstance

private fun ResponseCOHNCert.protoMergeImpl(plus: pbandk.Message?): ResponseCOHNCert = (plus as? ResponseCOHNCert)?.let {
    it.copy(
        result = plus.result ?: result,
        cert = plus.cert ?: cert,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseCOHNCert {
    var result: open_gopro.EnumResultGeneric? = null
    var cert: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> cert = _fieldValue as String
        }
    }

    return ResponseCOHNCert(result, cert, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetCOHNSetting")
public fun RequestSetCOHNSetting?.orDefault(): open_gopro.RequestSetCOHNSetting = this ?: RequestSetCOHNSetting.defaultInstance

private fun RequestSetCOHNSetting.protoMergeImpl(plus: pbandk.Message?): RequestSetCOHNSetting = (plus as? RequestSetCOHNSetting)?.let {
    it.copy(
        cohnActive = plus.cohnActive ?: cohnActive,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetCOHNSetting.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestSetCOHNSetting {
    var cohnActive: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> cohnActive = _fieldValue as Boolean
        }
    }

    return RequestSetCOHNSetting(cohnActive, unknownFields)
}
