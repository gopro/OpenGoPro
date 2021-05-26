/* CameraError.swift/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue May 18 22:08:51 UTC 2021 */

//
//  CameraError.swift
//  EnableWiFiDemo
//

import Foundation

/// A simple enum for describing the possible errors that may occur
enum CameraError: Error {
    case invalidRequest     // The request sent to the camera is not valid
    case invalidResponse    // The camera sent an invalid response
    case networkError       // Network error
    case responseError      // Response error
}
