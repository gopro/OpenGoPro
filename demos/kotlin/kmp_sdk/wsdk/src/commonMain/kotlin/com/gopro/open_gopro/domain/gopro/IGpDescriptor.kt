/* IGpDescriptor.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.CommunicationType
import com.gopro.open_gopro.GoProId
import com.gopro.open_gopro.operations.AccessPointState
import com.gopro.open_gopro.operations.CohnState
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow

/** Properties of a connectd GoPro */
interface IGpDescriptor {
  /** Identifier of connected GoPro */
  val id: GoProId

  /**
   * Is the camera busy performing an operation?
   *
   * @see [Busy Status](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8)
   */
  val isBusy: StateFlow<Boolean>

  /**
   * Is the camera currently encoding?
   *
   * @see
   *   [Encoding Status](https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10)
   */
  val isEncoding: StateFlow<Boolean>

  /**
   * Is the camera ready to communicate?
   *
   * That is, is both [isBusy] and [isEncoding] are false
   *
   * @see
   *   [Camera Readiness](https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#camera-readiness)
   */
  val isReady: StateFlow<Boolean>

  /**
   * State of the camera connecting to an Access Point
   *
   * That is, the camera will be operating in STA mode.
   *
   * @see [gopro.features.AccessPointFeature]
   */
  val accessPointState: StateFlow<AccessPointState>

  /**
   * State of COHN provisioning
   *
   * @see [gopro.features.CohnFeature]
   */
  val cohnState: StateFlow<CohnState>

  /** List of currently available communicators by [CommunicationType] */
  val communicators: List<CommunicationType>

  /** IP Address of connected device. Null if not HTTP connection is available. */
  val ipAddress: String?

  /** Disconnect notifications by [CommunicationType] */
  val disconnects: Flow<CommunicationType>

  val isBleAvailable: Boolean
  val isHttpAvailable: Boolean
}

internal interface GpDescriptorManager {
  fun getDescriptor(): IGpDescriptor

  fun setAccessPointState(state: AccessPointState)

  fun setCohnState(state: CohnState)
}
