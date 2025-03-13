/* operation.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.operations

import com.gopro.open_gopro.CommunicationType

class OperationUnsupportedForCommunicator(operation: String, communicationType: CommunicationType) :
    Exception("$operation not supported on $communicationType")

class ApiError(message: String) : Exception(message)

/** Represent SerializationExceptions. */
class SerializationError(message: String) : Exception("Http Network Error: $message")
