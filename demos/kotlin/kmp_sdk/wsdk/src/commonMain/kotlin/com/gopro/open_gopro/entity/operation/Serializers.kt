/* Serializers.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import kotlin.reflect.KClass
import kotlinx.serialization.DeserializationStrategy
import kotlinx.serialization.KSerializer
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.SerialDescriptor
import kotlinx.serialization.encodeToString
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonContentPolymorphicSerializer
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.modules.SerializersModule
import kotlinx.serialization.modules.contextual
import pbandk.ExperimentalProtoJson
import pbandk.json.encodeToJsonString

private abstract class IntEnumSerializer<T : IntEnum>(
    enumClass: KClass<T>,
    private val companion: IntEnumCompanion<T>
) : KSerializer<T> {

  override val descriptor: SerialDescriptor =
      PrimitiveSerialDescriptor(enumClass.simpleName!!, PrimitiveKind.INT)

  override fun deserialize(decoder: Decoder): T = companion.fromInt(decoder.decodeInt())

  override fun serialize(encoder: Encoder, value: T) = encoder.encodeInt(value.value)
}

private object WebcamErrorIntEnumSerializer :
    IntEnumSerializer<WebcamError>(WebcamError::class, WebcamError)

private object WebcamStatusIntEnumSerializer :
    IntEnumSerializer<WebcamStatus>(WebcamStatus::class, WebcamStatus)

/**
 * The main problem here is that the generated Protobuf enums are not JSON-serializable. So firstly
 * this requires a custom serializer for each enum.
 *
 * Furthermore, the pbandk protobuf library provides a json encoder however this nonconfigurably
 * writes the enum values using their string name. Our API however requires the enums, in the HTTP
 * request for example, to be integer values.
 *
 * Therefore we need 2 custom JSON serializers.
 *
 * TODO Verify that this kclass / reflect stuff works on iOS...
 */
private abstract class EnumProtoSerializerByValue<T : pbandk.Message.Enum>(
    enumClass: KClass<T>,
    private val enum: pbandk.Message.Enum.Companion<T>
) : KSerializer<T> {

  override val descriptor: SerialDescriptor =
      PrimitiveSerialDescriptor(enumClass.simpleName!!, PrimitiveKind.INT)

  override fun deserialize(decoder: Decoder): T = enum.fromValue(decoder.decodeString().toInt())

  override fun serialize(encoder: Encoder, value: T) = encoder.encodeString(value.value.toString())
}

private object EnumPresetGroupSerializerByValue :
    EnumProtoSerializerByValue<EnumPresetGroup>(EnumPresetGroup::class, EnumPresetGroup.Companion)

private object EnumPresetTitleSerializerByValue :
    EnumProtoSerializerByValue<EnumPresetTitle>(EnumPresetTitle::class, EnumPresetTitle.Companion)

private object EnumPresetIconSerializerByValue :
    EnumProtoSerializerByValue<EnumPresetIcon>(EnumPresetIcon::class, EnumPresetIcon.Companion)

private object EnumCohnStatusSerializerByValue :
    EnumProtoSerializerByValue<EnumCOHNStatus>(EnumCOHNStatus::class, EnumCOHNStatus.Companion)

private object EnumCohnNetworkStateSerializerByValue :
    EnumProtoSerializerByValue<EnumCOHNNetworkState>(
        EnumCOHNNetworkState::class, EnumCOHNNetworkState.Companion)

private object EnumPresetGroupIconSerializerByValue :
    EnumProtoSerializerByValue<EnumPresetGroupIcon>(
        EnumPresetGroupIcon::class, EnumPresetGroupIcon.Companion)

private object EnumFlatmodeSerializerByValue :
    EnumProtoSerializerByValue<EnumFlatMode>(EnumFlatMode::class, EnumFlatMode.Companion)

private abstract class EnumProtoSerializerByName<T : pbandk.Message.Enum>(
    private val enumClass: KClass<T>,
    private val enum: pbandk.Message.Enum.Companion<T>
) : KSerializer<T> {

  override val descriptor: SerialDescriptor =
      PrimitiveSerialDescriptor(enumClass.simpleName!!, PrimitiveKind.STRING)

  override fun deserialize(decoder: Decoder): T = enum.fromName(decoder.decodeString())

  override fun serialize(encoder: Encoder, value: T) =
      encoder.encodeString(
          value.name ?: throw Exception("Enum ${enumClass.simpleName!!} does not have a name."))
}

internal val jsonDefault = Json {
  serializersModule = SerializersModule {
    contextual(EnumPresetGroupSerializerByValue)
    contextual(EnumPresetTitleSerializerByValue)
    contextual(EnumPresetGroupIconSerializerByValue)
    contextual(EnumFlatmodeSerializerByValue)
    contextual(EnumPresetIconSerializerByValue)
    contextual(EnumCohnStatusSerializerByValue)
    contextual(EnumCohnNetworkStateSerializerByValue)
    contextual(WebcamErrorIntEnumSerializer)
    contextual(WebcamStatusIntEnumSerializer)
  }
}

private object EnumPresetGroupSerializerByName :
    EnumProtoSerializerByName<EnumPresetGroup>(EnumPresetGroup::class, EnumPresetGroup.Companion)

private object EnumPresetTitleSerializerByName :
    EnumProtoSerializerByName<EnumPresetTitle>(EnumPresetTitle::class, EnumPresetTitle.Companion)

private object EnumPresetIconSerializerByName :
    EnumProtoSerializerByName<EnumPresetIcon>(EnumPresetIcon::class, EnumPresetIcon.Companion)

private object EnumPresetGroupIconSerializerByName :
    EnumProtoSerializerByName<EnumPresetGroupIcon>(
        EnumPresetGroupIcon::class, EnumPresetGroupIcon.Companion)

private object EnumCohnStatusSerializerByName :
    EnumProtoSerializerByName<EnumCOHNStatus>(EnumCOHNStatus::class, EnumCOHNStatus.Companion)

private object EnumCohnNetworkStateSerializerByName :
    EnumProtoSerializerByName<EnumCOHNNetworkState>(
        EnumCOHNNetworkState::class, EnumCOHNNetworkState.Companion)

private object EnumFlatmodeSerializerByName :
    EnumProtoSerializerByName<EnumFlatMode>(EnumFlatMode::class, EnumFlatMode.Companion)

internal val jsonFromProto = Json {
  serializersModule = SerializersModule {
    contextual(EnumPresetGroupSerializerByName)
    contextual(EnumPresetTitleSerializerByName)
    contextual(EnumPresetGroupIconSerializerByName)
    contextual(EnumFlatmodeSerializerByName)
    contextual(EnumPresetIconSerializerByName)
    contextual(EnumCohnStatusSerializerByName)
    contextual(EnumCohnNetworkStateSerializerByName)
  }
}

@OptIn(ExperimentalProtoJson::class)
internal inline fun <reified O> serializeAsDefaultFromProto(proto: pbandk.Message): String =
    jsonDefault.encodeToString(jsonFromProto.decodeFromString<O>(proto.encodeToJsonString()))

internal object StringAsBooleanSerializer : KSerializer<Boolean> {
  override val descriptor: SerialDescriptor =
      PrimitiveSerialDescriptor("StringAsBoolean", PrimitiveKind.STRING)

  override fun serialize(encoder: Encoder, value: Boolean) =
      encoder.encodeString(if (value) "1" else "0")

  override fun deserialize(decoder: Decoder): Boolean =
      when (val value = decoder.decodeString()) {
        "0" -> false
        "1" -> true
        else -> throw Exception("Can not deserialize $value as a Boolean")
      }
}

// https://medium.com/livefront/intro-to-polymorphism-with-kotlinx-serialization-b8f5f1cedc99
internal object MediaMetadataSerializer :
    JsonContentPolymorphicSerializer<MediaMetadata>(
        MediaMetadata::class,
    ) {
  override fun selectDeserializer(
      element: JsonElement,
  ): DeserializationStrategy<MediaMetadata> {
    val jsonObject = element.jsonObject
    return when {
      jsonObject.containsKey("ao") -> VideoMediaMetadata.serializer()
      else -> PhotoMediaMetadata.serializer()
    }
  }
}

internal object MediaListItemSerializer :
    JsonContentPolymorphicSerializer<MediaListItem>(
        MediaListItem::class,
    ) {
  override fun selectDeserializer(
      element: JsonElement,
  ): DeserializationStrategy<MediaListItem> {
    val jsonObject = element.jsonObject
    return when {
      jsonObject.containsKey("g") -> GroupedMediaListItem.serializer()
      else -> SingleMediaListItem.serializer()
    }
  }
}
