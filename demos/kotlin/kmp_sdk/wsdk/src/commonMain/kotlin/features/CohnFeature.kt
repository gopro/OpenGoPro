package features

import co.touchlab.kermit.Logger
import domain.gopro.CohnState
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.transform
import open_gopro.EnumCOHNNetworkState
import open_gopro.EnumCOHNStatus
import operation.commands.CohnClearCert
import operation.commands.CohnCreateCert
import operation.commands.CohnGetCert
import operation.commands.CohnGetStatus

private val logger = Logger.withTag("CohnFeature")

class CohnFeature(featureContext: IFeatureContext): IFeatureContext by featureContext {
    private var ssid: String? = null
    private var password: String? = null
    private var username: String? = null
    private var ipAddress: String? = null
    private var certificate: String? = null

    suspend fun getCohnStatus(): Flow<CohnState> =
        gopro.commands.getCohnStatus().getOrThrow().transform { update ->
            update.password?.let { password = it }
            update.ssid?.let { ssid = it }
            update.ipAddress?.let { ipAddress = it }
            update.username?.let { username = it }
            logger.i("Received COHN status: $update")
            if ((update.state == EnumCOHNNetworkState.COHN_STATE_NETWORK_CONNECTED) && (update.status == EnumCOHNStatus.COHN_PROVISIONED)) {
                logger.i("COHN provisioned. Getting certificate.")
                certificate = gopro.commands.getCohnCertificate().getOrThrow()
                emit(
                    CohnState.Provisioned(
                        username = username!!,
                        password = password!!,
                        ipAddress = ipAddress!!,
                        certificates = listOf(certificate!!) // TODO how to handle multiple?
                    )
                )
            } // TODO remove from DB on unprovision
            else {
                emit(CohnState.Unprovisioned)
            }
        }

    suspend fun provisionCohn(): Result<CohnState.Provisioned> {
        // Start fresh by clearing cert
        logger.i("Clearing COHN Certificate for new provision")
        gopro.commands.clearCohnCertificate().onFailure { return Result.failure(it) }

        // Provision
        logger.i("Requesting new COHN cert creation to provision COHN")
        gopro.commands.createCohnCertificate(true)

        // Wait for provisioning to be complete and results to accumulate
        // TODO timeout here?
        logger.i("Waiting for COHN provisioning to complete...")
        val provisionedState =
            getCohnStatus().first { it is CohnState.Provisioned } as CohnState.Provisioned
        logger.i("Storing COHN credentials to disk")
        cameraRepo.addHttpsCredentials(gopro.serialId, provisionedState)
        return Result.success(provisionedState)
    }
}