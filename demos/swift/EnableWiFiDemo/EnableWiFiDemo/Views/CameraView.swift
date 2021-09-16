/* CameraView.swift/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:10 PM */

//
//  CameraView.swift
//  EnableWiFiDemo
//

import SwiftUI
import NetworkExtension

struct CameraView: View {
    var peripheral: Peripheral?
    var body: some View {
        Button(action: {
            NSLog("Enabling WiFi...")
            peripheral?.enableWiFi { error in
                if error != nil {
                    print("\(error!)")
                    return
                }

                NSLog("Requesting WiFi settings...")
                peripheral?.requestWiFiSettings { result in
                    switch result {
                    case .success(let wifiSettings):
                        joinWiFi(with: wifiSettings.SSID, password: wifiSettings.password)
                    case .failure(let error):
                        print("\(error)")
                    }
                }
            }
        }, label: {
            Text("Enable Wi-Fi")
        })
        .toolbar {
            ToolbarItem(placement: .principal) {
                Text(peripheral?.name ?? "").fontWeight(.bold)
            }
        }
    }

    private func joinWiFi(with SSID: String, password: String) {
        NSLog("Joining WiFi \(SSID)...")
        let configuration = NEHotspotConfiguration(ssid: SSID, passphrase: password, isWEP: false)
        NEHotspotConfigurationManager.shared.removeConfiguration(forSSID: SSID)
        configuration.joinOnce = false
        NEHotspotConfigurationManager.shared.apply(configuration) { error in
            guard let error = error else { NSLog("Joining WiFi succeeded"); return }
            NSLog("Joining WiFi failed: \(error)")
        }
    }
}

struct CameraView_Previews: PreviewProvider {
    static var previews: some View {
        CameraView()
    }
}
