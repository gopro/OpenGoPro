package extensions

import entity.communicator.CommunicationType

internal fun List<CommunicationType>.bleIfAvailable(): CommunicationType? =
    this.firstOrNull { it == CommunicationType.BLE }

internal fun List<CommunicationType>.httpIfAvailable(): CommunicationType? =
    this.firstOrNull { (it == CommunicationType.HTTP) }