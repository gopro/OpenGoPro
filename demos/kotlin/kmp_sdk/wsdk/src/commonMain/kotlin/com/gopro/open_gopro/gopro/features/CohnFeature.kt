/* CohnFeature.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import co.touchlab.kermit.Logger
import com.gopro.open_gopro.OgpSdkIsolatedKoinContext
import com.gopro.open_gopro.domain.data.ICameraRepository
import com.gopro.open_gopro.operations.CohnState
import com.gopro.open_gopro.operations.EnumCOHNNetworkState
import com.gopro.open_gopro.operations.EnumCOHNStatus
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.transform
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import org.koin.core.component.KoinComponent

private val logger = Logger.withTag("CohnFeature")

/**
 * Camera-on-the-home-network (COHN) provisioning and querying
 *
 * @property context feature context
 * @see [Camera on the Home Network](https://gopro.github.io/OpenGoPro/ble/features/cohn.html)
 */
class CohnFeature internal constructor(private val context: IFeatureContext) : KoinComponent {
  private var ssid: String? = null
  private var password: String? = null
  private var username: String? = null
  private var ipAddress: String? = null
  private var certificate: String? = null

  private val _state: MutableStateFlow<CohnState> = MutableStateFlow(CohnState.Unprovisioned)
  val state: StateFlow<CohnState>
    get() = _state

  private val cameraRepo: ICameraRepository = OgpSdkIsolatedKoinContext.getOgpSdkKoinApp().get()

  init {
    context.scope.launch {
      while (!context.gopro.isBleAvailable) {
        delay(500) // Wait for BLE to be available
        if (!isActive) {
          return@launch
        }
      }
      getState().collect { cohnState ->
        logger.d("COHN Feature updating state: $cohnState")
        _state.update { cohnState }
      }
    }
  }

  /**
   * Get the continuous COHN State
   *
   * @return flow of COHN States
   * @see
   *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/cohn.html#get-cohn-status)
   */
  private suspend fun getState(): Flow<CohnState> =
      context.gopro.commands.getCohnStatus().getOrThrow().transform { update ->
        logger.i("Received COHN status: $update")

        val isProvisionedStatus =
            ((update.state == EnumCOHNNetworkState.COHN_STATE_NETWORK_CONNECTED) &&
                (update.status == EnumCOHNStatus.COHN_PROVISIONED))

        if ((_state.value == CohnState.Unprovisioned) && isProvisionedStatus) {
          update.password?.let { password = it }
          update.ssid?.let { ssid = it }
          update.ipAddress?.let { ipAddress = it }
          update.username?.let { username = it }
          logger.i("COHN provisioned. Getting certificate")
          context.gopro.commands
              .getCohnCertificate()
              .onFailure { logger.e("Failed to get COHN certificate") }
              .onSuccess { certificate = it }
          emit(
              CohnState.Provisioned(
                  username = username!!,
                  password = password!!,
                  ipAddress = ipAddress!!,
                  certificates = listOf(certificate!!)))
        } // TODO remove from DB on unprovision
        else {
          emit(CohnState.Unprovisioned)
        }
      }

  suspend fun unprovision(): Result<Unit> = context.gopro.commands.clearCohnCertificate().map {}

  suspend fun enable(): Result<Unit> = context.gopro.commands.setCohnSetting(disableCohn = false)

  suspend fun disable(): Result<Unit> = context.gopro.commands.setCohnSetting(disableCohn = true)

  /**
   * Provision camera for COHN
   *
   * This will clear any existing COHN credentials, (re)provision, then return the credentials
   *
   * @return provisioning credentials
   */
  suspend fun provision(): Result<CohnState.Provisioned> {
    unprovision().onFailure {
      return Result.failure(it)
    }

    // Provision
    logger.i("Requesting new COHN cert creation to provision COHN")
    context.gopro.commands.createCohnCertificate(true)

    // Wait for provisioning to be complete and results to accumulate
    // TODO timeout here?
    logger.i("Waiting for COHN provisioning to complete...")
    val provisionedState = state.first { it is CohnState.Provisioned } as CohnState.Provisioned
    logger.i("Storing COHN credentials to disk")
    cameraRepo.addHttpsCredentials(context.gopro.id, provisionedState)
    return Result.success(provisionedState)
  }
}
