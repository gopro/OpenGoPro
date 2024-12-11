package com.gopro.open_gopro.entity.operation

enum class CameraControlStatus(val value: Int) {
    IDLE(0),
    CAMERA(2),
    EXTERNAL(3),
    COF_SETUP(4);

    companion object {
        fun fromValue(value: Int) = CameraControlStatus.entries.firstOrNull { it.value == value }
    }
}