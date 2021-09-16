/* Peripheral+Camera.swift/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:08 PM */

//
//  Peripheral+Camera.swift
//  EnableWiFiDemo
//

import Foundation
import CoreBluetooth

/// A struct representing the camera's Wi-Fi settings
struct WiFiSettings {
    var SSID: String
    let password: String
}

extension Peripheral {

    /// Turns ON camera's Wi-Fi
    /// - Parameter completion: The completion handler with an optional error that is invoked once the request completes.
    ///
    /// Discussion:
    /// In order to turn on the camera's Wi-Fi, the first thing to do is to enable the notification on the
    /// characteristic GP-0073 and then write 03:17:01:01 to the characteristic GP-0072

    func enableWiFi(_ completion: ((Error?) -> Void)?) {

        let serviceUUID = CBUUID(string: "FEA6")
        let commandUUID = CBUUID(string: "B5F90072-AA8D-11E3-9046-0002A5D5C51B")
        let commandResponseUUID = CBUUID(string: "B5F90073-AA8D-11E3-9046-0002A5D5C51B")
        let data = Data([0x03, 0x17, 0x01, 0x01])

        let finishWithError: (Error?) -> Void = { error in
            // make sure to dispatch the result on the main thread
            DispatchQueue.main.async {
                completion?(error)
            }
        }

        registerObserver(serviceUUID: serviceUUID, characteristicUUID: commandResponseUUID) { data in

            // The response to the command to enable Wi-Fi is expected to be 3 bytes
            if data.count != 3 {
                finishWithError(CameraError.invalidResponse)
                return
            }

            // The third byte represents the camera response. If the byte is 0x00 then the request was successful
            finishWithError(data[2] == 0x00 ? nil : CameraError.responseError)

        } completion: { [weak self] error in
            // Check that we successfully enable the notification for the response before writing to the characteristic
            if error != nil { finishWithError(error); return }
            self?.write(data: data, serviceUUID: serviceUUID, characteristicUUID: commandUUID) { error in
                if error != nil { finishWithError(error) }
            }
        }
    }

    /// Reads camera's Wi-Fi settings
    /// - Parameter completion: The completion handler with a result representing either a success or a failure.
    ///                         In the success case, the associated value is an instance of WiFiSettings
    ///
    /// Discussion:
    /// Requesting Wi-Fi setting consists in reading characteristics GP-0002 (SSID) and GP-0003 (password)
    /// on the GoPro WiFi Access Point service

    func requestWiFiSettings(_ completion: ((Result<WiFiSettings, Error>) -> Void)?) {
        let serviceUUID = CBUUID(string: "B5F90001-AA8D-11E3-9046-0002A5D5C51B")
        var SSID: String?
        var password: String?

        let finishWithResult: (Result<WiFiSettings, Error>) -> Void = { result in
            // make sure to dispatch the result on the main thread
            DispatchQueue.main.async {
                completion?(result)
            }
        }

        let reads = DispatchGroup()
        reads.enter()
        readData(from: CBUUID(string: "B5F90002-AA8D-11E3-9046-0002A5D5C51B"), serviceUUID: serviceUUID) { result in
            switch result {
            case .success(let data):
                // we got the data, let's convert to a string
                SSID = String(bytes: data.subdata(in: 0..<data.count), encoding: .utf8)
            case .failure(let error):
                finishWithResult(.failure(error))
            }
            reads.leave()
        }

        reads.enter()
        readData(from: CBUUID(string: "B5F90003-AA8D-11E3-9046-0002A5D5C51B"), serviceUUID: serviceUUID) { result in
            switch result {
            case .success(let data):
                // we got the data, let's convert to a string
                password = String(bytes: data.subdata(in: 0..<data.count), encoding: .utf8)
            case .failure(let error):
                finishWithResult(.failure(error))
            }
            reads.leave()
        }

        reads.notify(queue: .main) {
            guard let SSID = SSID, let password = password else {
                finishWithResult(.failure(CameraError.invalidResponse))
                return
            }

            finishWithResult(.success(WiFiSettings(SSID: SSID, password: password)))
        }
    }
}
