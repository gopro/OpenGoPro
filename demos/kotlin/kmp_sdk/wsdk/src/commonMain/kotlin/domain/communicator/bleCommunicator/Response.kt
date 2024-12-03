package domain.communicator.bleCommunicator

import entity.communicator.ActionId
import entity.communicator.CommandId
import entity.communicator.FeatureId
import entity.communicator.QueryId
import entity.communicator.responseProtobufIds
import entity.network.ble.GpUuid
import entity.queries.SettingId
import entity.queries.StatusId


internal sealed interface ResponseId {
    val shouldBeMatchedAsSynchronousResponse: Boolean
    val shouldBeForwardedAsNotification: Boolean

    data class Protobuf(val featureId: FeatureId, val actionId: ActionId) : ResponseId {
        override val shouldBeMatchedAsSynchronousResponse = true
        override val shouldBeForwardedAsNotification = true
        override fun toString() = "Protobuf Response: $featureId::$actionId"
    }

    data class Command(val id: CommandId) : ResponseId {
        override val shouldBeMatchedAsSynchronousResponse = true
        override val shouldBeForwardedAsNotification = true
        override fun toString(): String = "Command Response: $id"
    }

    data class Setting(val id: SettingId) : ResponseId {
        override val shouldBeMatchedAsSynchronousResponse = true
        override val shouldBeForwardedAsNotification = true
        override fun toString(): String = "Set Setting Response: $id"
    }

    open class Query(val id: QueryId) : ResponseId {
        override fun toString(): String = "Query Response: $id"

        final override val shouldBeForwardedAsNotification = when (id) {
            QueryId.ASYNC_SETTING_VALUE_NOTIFICATION,
            QueryId.ASYNC_STATUS_VALUE_NOTIFICATION,
            QueryId.ASYNC_SETTING_CAPABILITY_NOTIFICATION -> true

            else -> false
        }
        override val shouldBeMatchedAsSynchronousResponse = !shouldBeForwardedAsNotification

        val isSetting = when (id) {
            QueryId.GET_SETTING_VALUES,
            QueryId.GET_SETTING_CAPABILITIES,
            QueryId.ASYNC_SETTING_CAPABILITY_NOTIFICATION,
            QueryId.ASYNC_SETTING_VALUE_NOTIFICATION,
            QueryId.REGISTER_SETTING_VALUE_UPDATES,
            QueryId.UNREGISTER_SETTING_VALUE_UPDATES,
            QueryId.REGISTER_SETTING_CAPABILITY_UPDATES,
            QueryId.UNREGISTER_SETTING_CAPABILITY_UPDATES -> true

            else -> false
        }

        val isStatus = when (id) {
            QueryId.GET_STATUS_VALUES,
            QueryId.ASYNC_STATUS_VALUE_NOTIFICATION,
            QueryId.UNREGISTER_STATUS_VALUE_UPDATES,
            QueryId.REGISTER_STATUS_VALUE_UPDATES -> true

            else -> false
        }

        val shouldBeSliced = when (id) {
            QueryId.GET_SETTING_CAPABILITIES,
            QueryId.ASYNC_SETTING_CAPABILITY_NOTIFICATION,
            QueryId.REGISTER_SETTING_CAPABILITY_UPDATES -> false

            else -> true
        }
    }

    data class QuerySetting(val queryId: QueryId, val settingId: SettingId) : Query(queryId) {
        override fun toString(): String = "Setting Query Response: $queryId ==> $settingId"
    }

    data class QueryStatus(val queryId: QueryId, val statusId: StatusId) : Query(queryId) {
        override fun toString(): String = "Status Query Response: $queryId ==> $statusId"
    }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun decipherResponse(message: IGpBleResponse): ResponseId {
    // Is it a Protobuf message?
    FeatureId.fromUByte(message.payload[0])?.let { featureId ->
        ActionId.fromUByte(message.payload[1])?.let { actionId ->
            if (responseProtobufIds.contains(featureId to actionId)) {
                return ResponseId.Protobuf(featureId, actionId)
            }
        }
    }
    // It is a TLV response since it is not a protobuf response. Decipher based on received UUID
    return when (message.uuid) {
        GpUuid.CQ_COMMAND_RESP -> ResponseId.Command(
            CommandId.fromUByte(message.payload[0])
                ?: throw Exception("Unexpected command ID ${message.payload[0]}")
        )

        GpUuid.CQ_SETTINGS_RESP -> ResponseId.Setting(SettingId.fromUByte(message.payload[0]))

        GpUuid.CQ_QUERY_RESP -> ResponseId.Query(QueryId.fromUByte(message.payload[0]))

        else -> throw Exception("Unable to decipher response for $message")
    }
}
