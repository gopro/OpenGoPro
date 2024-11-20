package gopro.features

import WsdkIsolatedKoinContext
import co.touchlab.kermit.Logger
import domain.data.ICameraRepository
import entity.operation.CohnState
import entity.operation.proto.EnumCOHNNetworkState
import entity.operation.proto.EnumCOHNStatus
import gopro.IFeatureContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.transform
import org.koin.core.component.KoinComponent

private val logger = Logger.withTag("CohnFeature")

/**
 * Camera-on-the-home-network (COHN) provisioning and querying
 *
 * @see [Camera on the Home Network](https://gopro.github.io/OpenGoPro/ble/features/cohn.html)
 *
 * @property context feature context
 */
class CohnFeature internal constructor(private val context: IFeatureContext) : KoinComponent {
    private var ssid: String? = null
    private var password: String? = null
    private var username: String? = null
    private var ipAddress: String? = null
    private var certificate: String? = null

    private val cameraRepo: ICameraRepository = WsdkIsolatedKoinContext.getWsdkKoinApp().get()

    /**
     * Get the continuous COHN State
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/cohn.html#get-cohn-status)
     *
     * @return flow of COHN States
     */
    suspend fun getStatus(): Flow<CohnState> =
        context.gopro.commands.getCohnStatus().getOrThrow().transform { update ->
            update.password?.let { password = it }
            update.ssid?.let { ssid = it }
            update.ipAddress?.let { ipAddress = it }
            update.username?.let { username = it }
            logger.i("Received COHN status: $update")
            if ((update.state == EnumCOHNNetworkState.COHN_STATE_NETWORK_CONNECTED) && (update.status == EnumCOHNStatus.COHN_PROVISIONED)) {
                logger.i("COHN provisioned. Getting certificate.")
                certificate = context.gopro.commands.getCohnCertificate().getOrThrow()
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

    suspend fun unprovision(): Result<Unit> = context.gopro.commands.clearCohnCertificate().map { }

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
        unprovision().onFailure { return Result.failure(it) }

        // Provision
        logger.i("Requesting new COHN cert creation to provision COHN")
        context.gopro.commands.createCohnCertificate(true)

        // Wait for provisioning to be complete and results to accumulate
        // TODO timeout here?
        logger.i("Waiting for COHN provisioning to complete...")
        val provisionedState =
            getStatus().first { it is CohnState.Provisioned } as CohnState.Provisioned
        logger.i("Storing COHN credentials to disk")
        cameraRepo.addHttpsCredentials(context.gopro.id, provisionedState)
        return Result.success(provisionedState)
    }
}