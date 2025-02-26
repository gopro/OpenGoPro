/* PresetUpdateCustom.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:28 UTC 2025 */

package com.gopro.open_gopro.operations.commands

import com.gopro.open_gopro.domain.api.BaseOperation
import com.gopro.open_gopro.domain.communicator.BleCommunicator
import com.gopro.open_gopro.domain.communicator.HttpCommunicator
import com.gopro.open_gopro.domain.communicator.bleCommunicator.ResponseId
import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.network.ble.GpUuid
import com.gopro.open_gopro.operations.EnumPresetIcon
import com.gopro.open_gopro.operations.EnumPresetTitle
import com.gopro.open_gopro.operations.RequestCustomPresetUpdate
import com.gopro.open_gopro.operations.UpdateCustomPresetRequest
import com.gopro.open_gopro.util.extensions.mapFromGenericProtoResponseToResult
import io.ktor.client.call.body
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.http.path
import pbandk.encodeToByteArray

internal class UpdateCustomPresetIcon(val icon: EnumPresetIcon) :
    BaseOperation<Unit>("Update Custom Preset Icon") {

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator
          .executeProtobufCommand(
              FeatureId.COMMAND,
              ActionId.REQUEST_PRESET_UPDATE_CUSTOM,
              RequestCustomPresetUpdate(iconId = icon).encodeToByteArray(),
              ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_PRESET_UPDATE_CUSTOM),
              GpUuid.CQ_COMMAND)
          .mapFromGenericProtoResponseToResult()

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .get {
            contentType(ContentType.Application.Json)
            url { path("gopro/camera/presets/update_custom") }
            setBody(UpdateCustomPresetRequest(iconId = icon.value))
          }
          .map { it.body() }
}

internal class UpdateCustomPresetTitle(val titleId: EnumPresetTitle) :
    BaseOperation<Unit>("Update Custom Preset Title") {

  private var customTitle: String? = null

  constructor(title: String) : this(EnumPresetTitle.PRESET_TITLE_CUSTOM) {
    customTitle = title
  }

  override suspend fun execute(communicator: BleCommunicator): Result<Unit> =
      communicator
          .executeProtobufCommand(
              FeatureId.COMMAND,
              ActionId.REQUEST_PRESET_UPDATE_CUSTOM,
              RequestCustomPresetUpdate(titleId = titleId, customName = customTitle)
                  .encodeToByteArray(),
              ResponseId.Protobuf(FeatureId.COMMAND, ActionId.RESPONSE_PRESET_UPDATE_CUSTOM),
              GpUuid.CQ_COMMAND)
          .mapFromGenericProtoResponseToResult()

  override suspend fun execute(communicator: HttpCommunicator): Result<Unit> =
      communicator
          .get {
            contentType(ContentType.Application.Json)
            url { path("gopro/camera/presets/update_custom") }
            setBody(UpdateCustomPresetRequest(titleId = titleId.value, name = customTitle))
          }
          .map { it.body() }
}
