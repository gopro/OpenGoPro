/* CameraControl.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

enum class CameraControlStatus(val value: Int) {
  IDLE(0),
  CAMERA(2),
  EXTERNAL(3),
  COF_SETUP(4);

  companion object {
    fun fromValue(value: Int) = CameraControlStatus.entries.firstOrNull { it.value == value }
  }
}
