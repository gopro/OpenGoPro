package com.gopro.open_gopro.operations

import com.gopro.open_gopro.CommunicationType

class OperationUnsupportedForCommunicator(operation: String, communicationType: CommunicationType) :
    Exception("$operation not supported on $communicationType")

class ApiError(message: String) : Exception(message)

/**
 * Represent SerializationExceptions.
 */
class SerializationError(message: String) : Exception("Http Network Error: $message")
