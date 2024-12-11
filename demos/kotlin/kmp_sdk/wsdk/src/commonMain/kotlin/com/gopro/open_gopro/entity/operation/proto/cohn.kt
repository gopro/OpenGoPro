@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.entity.operation.proto

@pbandk.Export
sealed class EnumCOHNStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCOHNStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object COHN_UNPROVISIONED : EnumCOHNStatus(0, "COHN_UNPROVISIONED")
    internal object COHN_PROVISIONED : EnumCOHNStatus(1, "COHN_PROVISIONED")
    internal class UNRECOGNIZED(value: Int) : EnumCOHNStatus(value)

    internal companion object : pbandk.Message.Enum.Companion<com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus> {
        internal val values: List<com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus> by lazy { listOf(COHN_UNPROVISIONED, COHN_PROVISIONED) }
        override fun fromValue(value: Int): com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCOHNStatus with name: $name")
    }
}

@pbandk.Export
sealed class EnumCOHNNetworkState(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCOHNNetworkState.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object COHN_STATE_INIT : EnumCOHNNetworkState(0, "COHN_STATE_Init")
    internal object COHN_STATE_ERROR : EnumCOHNNetworkState(1, "COHN_STATE_Error")
    internal object COHN_STATE_EXIT : EnumCOHNNetworkState(2, "COHN_STATE_Exit")
    internal object COHN_STATE_IDLE : EnumCOHNNetworkState(5, "COHN_STATE_Idle")
    internal object COHN_STATE_NETWORK_CONNECTED : EnumCOHNNetworkState(27, "COHN_STATE_NetworkConnected")
    internal object COHN_STATE_NETWORK_DISCONNECTED : EnumCOHNNetworkState(28, "COHN_STATE_NetworkDisconnected")
    internal object COHN_STATE_CONNECTING_TO_NETWORK : EnumCOHNNetworkState(29, "COHN_STATE_ConnectingToNetwork")
    internal object COHN_STATE_INVALID : EnumCOHNNetworkState(30, "COHN_STATE_Invalid")
    internal class UNRECOGNIZED(value: Int) : EnumCOHNNetworkState(value)

    internal companion object : pbandk.Message.Enum.Companion<com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState> {
        internal val values: List<com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState> by lazy { listOf(COHN_STATE_INIT, COHN_STATE_ERROR, COHN_STATE_EXIT, COHN_STATE_IDLE, COHN_STATE_NETWORK_CONNECTED, COHN_STATE_NETWORK_DISCONNECTED, COHN_STATE_CONNECTING_TO_NETWORK, COHN_STATE_INVALID) }
        override fun fromValue(value: Int): com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCOHNNetworkState with name: $name")
    }
}

@pbandk.Export
internal data class RequestGetCOHNStatus(
    val registerCohnStatus: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus by lazy { com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus = com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetCOHNStatus",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "register_cohn_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "registerCohnStatus",
                        value = com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus::registerCohnStatus
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class NotifyCOHNStatus(
    val status: com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus? = null,
    val state: com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState? = null,
    val username: String? = null,
    val password: String? = null,
    val ipaddress: String? = null,
    val enabled: Boolean? = null,
    val ssid: String? = null,
    val macaddress: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus by lazy { com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyCOHNStatus",
            messageClass = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::class,
            messageCompanion = this,
            fields = buildList(8) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus.Companion, hasPresence = true),
                        jsonName = "status",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::status
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "state",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState.Companion, hasPresence = true),
                        jsonName = "state",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::state
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "username",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "username",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::username
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "password",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "password",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::password
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ipaddress",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ipaddress",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::ipaddress
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "enabled",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "enabled",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::enabled
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "ssid",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "ssid",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::ssid
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "macaddress",
                        number = 8,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "macaddress",
                        value = com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus::macaddress
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestCreateCOHNCert(
    val override: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert by lazy { com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert = com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCreateCOHNCert",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "override",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "override",
                        value = com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert::override
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestClearCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert by lazy { com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert = com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestClearCOHNCert",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
internal data class RequestCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert by lazy { com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert = com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCOHNCert",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
internal data class ResponseCOHNCert(
    val result: com.gopro.open_gopro.entity.operation.proto.EnumResultGeneric? = null,
    val cert: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert by lazy { com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert = com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseCOHNCert",
            messageClass = com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "cert",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "cert",
                        value = com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert::cert
                    )
                )
            }
        )
    }
}

@pbandk.Export
internal data class RequestSetCOHNSetting(
    val cohnActive: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting by lazy { com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting = com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCOHNSetting",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "cohn_active",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "cohnActive",
                        value = com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting::cohnActive
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetCOHNStatus")
internal fun RequestGetCOHNStatus?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestGetCOHNStatus = this ?: RequestGetCOHNStatus.defaultInstance

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
internal fun NotifyCOHNStatus?.orDefault(): com.gopro.open_gopro.entity.operation.proto.NotifyCOHNStatus = this ?: NotifyCOHNStatus.defaultInstance

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
    var status: com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus? = null
    var state: com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState? = null
    var username: String? = null
    var password: String? = null
    var ipaddress: String? = null
    var enabled: Boolean? = null
    var ssid: String? = null
    var macaddress: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> status = _fieldValue as com.gopro.open_gopro.entity.operation.proto.EnumCOHNStatus
            2 -> state = _fieldValue as com.gopro.open_gopro.entity.operation.proto.EnumCOHNNetworkState
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
internal fun RequestCreateCOHNCert?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestCreateCOHNCert = this ?: RequestCreateCOHNCert.defaultInstance

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
internal fun RequestClearCOHNCert?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestClearCOHNCert = this ?: RequestClearCOHNCert.defaultInstance

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
internal fun RequestCOHNCert?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestCOHNCert = this ?: RequestCOHNCert.defaultInstance

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
internal fun ResponseCOHNCert?.orDefault(): com.gopro.open_gopro.entity.operation.proto.ResponseCOHNCert = this ?: ResponseCOHNCert.defaultInstance

private fun ResponseCOHNCert.protoMergeImpl(plus: pbandk.Message?): ResponseCOHNCert = (plus as? ResponseCOHNCert)?.let {
    it.copy(
        result = plus.result ?: result,
        cert = plus.cert ?: cert,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseCOHNCert {
    var result: com.gopro.open_gopro.entity.operation.proto.EnumResultGeneric? = null
    var cert: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as com.gopro.open_gopro.entity.operation.proto.EnumResultGeneric
            2 -> cert = _fieldValue as String
        }
    }

    return ResponseCOHNCert(result, cert, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetCOHNSetting")
internal fun RequestSetCOHNSetting?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestSetCOHNSetting = this ?: RequestSetCOHNSetting.defaultInstance

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
