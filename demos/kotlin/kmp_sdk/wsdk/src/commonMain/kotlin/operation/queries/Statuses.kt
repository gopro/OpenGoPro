package operation.queries

import domain.api.BaseOperation
import domain.api.IOperationMarshaller
import domain.communicator.BleCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.QueryId
import entity.constants.StatusId
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

@OptIn(ExperimentalUnsignedTypes::class)
class StatusFacade<T : Any>(
    private val statusId: StatusId,
    private val marshaller: IOperationMarshaller,
    private val fromUByteArray: (UByteArray) -> T
) {
    // TODO lazy init these classes

    private inner class GetStatusValue : BaseOperation<T>("Get Status Value::${statusId.name}") {
        override suspend fun execute(communicator: BleCommunicator): Result<T> =
            communicator.executeQuery(QueryId.GET_STATUS_VALUES, statusId)
                .map { fromUByteArray(it) }
    }

    private inner class RegisterForStatusValueUpdates :
        BaseOperation<Pair<T, Flow<T>>>("Register Status Value Updates::${statusId.name}") {

        override suspend fun execute(communicator: BleCommunicator): Result<Pair<T, Flow<T>>> {
            // Send initial query OTA to register and store current value for later returning
            val currentValue =
                communicator.executeQuery(
                    QueryId.REGISTER_STATUS_VALUE_UPDATES,
                    statusId
                )
                    .fold(
                        onFailure = { return Result.failure(it) },
                        onSuccess = { fromUByteArray(it) },
                    )

            // Now actually register to receive notifications
            return communicator.registerUpdate(
                ResponseId.QueryStatus(
                    QueryId.ASYNC_STATUS_VALUE_NOTIFICATION,
                    statusId
                )
            ).map { flow -> currentValue to flow.map { fromUByteArray(it.payload) } }
        }
    }

// TODO strategies here?

    suspend fun getValue(): Result<T> = marshaller.marshal(GetStatusValue())

    // TODO | can we always allow fastpass here? It's needed to set up initial state querying.
    // TODO | If not, need to add initializing in descriptor.
    suspend fun registerValueUpdate(): Result<Pair<T, Flow<T>>> =
        marshaller.marshal(RegisterForStatusValueUpdates()) {
            isFastpass { _, _ -> true }
            useCommunicator { _, _ -> entity.communicator.CommunicationType.BLE }
        }

    suspend fun registerCapabilityUpdates(): Result<Flow<T>> = TODO()
}
