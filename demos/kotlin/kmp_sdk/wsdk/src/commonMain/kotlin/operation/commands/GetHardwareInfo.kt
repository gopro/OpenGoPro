package operation.commands

import domain.api.BaseOperation
import domain.communicator.BleCommunicator
import domain.communicator.HttpCommunicator
import domain.communicator.bleCommunicator.ResponseId
import entity.communicator.CommandId
import entity.operation.HardwareInfo
import extensions.decodeToString
import io.ktor.client.call.body
import io.ktor.http.path

@OptIn(ExperimentalUnsignedTypes::class)
internal class GetHardwareInfo : BaseOperation<HardwareInfo>("Get Hardware Info") {
    override suspend fun execute(communicator: BleCommunicator): Result<HardwareInfo> =
        communicator.executeTlvCommand(
            CommandId.GET_HARDWARE_INFO,
            ResponseId.Command(CommandId.GET_HARDWARE_INFO),
        ).map { parseBleCommunicatorResponse(it) }

    override suspend fun execute(communicator: HttpCommunicator): Result<HardwareInfo> =
        communicator.get { url { path("gopro/camera/info") } }.map { it.body() }
}

@OptIn(ExperimentalUnsignedTypes::class)
internal fun parseBleCommunicatorResponse(response: UByteArray): HardwareInfo {
    var buf = response.toList()

    val modelNumberLen = buf.first().toInt()
    buf = buf.drop(1)
    val modelNumber = buf.slice(0..<modelNumberLen).toUByteArray().decodeToString()
    buf = buf.drop(modelNumberLen)

    val modelNameLen = buf.first().toInt()
    buf = buf.drop(1)
    val modelName = buf.slice(0..<modelNameLen).toUByteArray().decodeToString()
    buf = buf.drop(modelNameLen)

    val deprecatedLen = buf.first().toInt()
    buf = buf.drop(1 + deprecatedLen)

    val firmwareVersionLen = buf.first().toInt()
    buf = buf.drop(1)
    val firmwareVersion = buf.slice(0..<firmwareVersionLen).toUByteArray().decodeToString()
    buf = buf.drop(firmwareVersionLen)

    val serialNumberLen = buf.first().toInt()
    buf = buf.drop(1)
    val serialNumber = buf.slice(0..<serialNumberLen).toUByteArray().decodeToString()
    buf = buf.drop(serialNumberLen)

    val apSsidLen = buf.first().toInt()
    buf = buf.drop(1)
    val apSsid = buf.slice(0..<apSsidLen).toUByteArray().decodeToString()
    buf = buf.drop(apSsidLen)

    val apMacAddressLen = buf.first().toInt()
    buf = buf.drop(1)
    val apMacAddress = buf.slice(0..<apMacAddressLen).toUByteArray().decodeToString()

    return HardwareInfo(
        modelNumber,
        modelName,
        firmwareVersion,
        serialNumber,
        apSsid,
        apMacAddress
    )
}