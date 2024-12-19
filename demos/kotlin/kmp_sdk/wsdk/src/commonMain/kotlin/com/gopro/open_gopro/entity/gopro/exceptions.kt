package com.gopro.open_gopro.gopro

class CameraInternalError(errorMessage: String) :
    Exception("Camera replied with error: $errorMessage")