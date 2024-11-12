package extensions

import entity.communicator.CommunicationType

fun List<CommunicationType>.bleIfAvailable(): CommunicationType? =
    this.firstOrNull { it == CommunicationType.BLE }

fun List<CommunicationType>.httpIfAvailable(): CommunicationType? =
    this.firstOrNull { (it == CommunicationType.HTTP) }