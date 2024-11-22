package exceptions

import entity.communicator.CommunicationType

class OperationUnsupportedForCommunicator(operation: String, communicationType: CommunicationType) :
    Exception("$operation not supported on $communicationType")

class DeviceNotFound(deviceId: String) :
    Exception("$deviceId not found")

class ApiError(message: String) : Exception(message)

class BleError(errorMessage: String) : Exception(errorMessage)

class CameraInternalError(errorMessage: String) :
    Exception("Camera replied with error: $errorMessage")

/**
 * Represents server (50x) and client (40x) errors.
 */
class HttpError(code: Int, errorMessage: String) :
    Exception("HTTP failed with status $code: $errorMessage")

/**
 * Represent IOExceptions and connectivity issues.
 */
class NetworkError(message: String) : Exception("Http Network Error: $message")

/**
 * Represent SerializationExceptions.
 */
class SerializationError(message: String) : Exception("Http Network Error: $message")