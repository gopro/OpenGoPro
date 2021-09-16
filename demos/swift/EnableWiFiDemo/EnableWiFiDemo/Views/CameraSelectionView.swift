/* CameraSelectionView.swift/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:10 PM */

//
//  CameraSelectionView.swift
//  EnableWiFiDemo
//

import SwiftUI
import CoreBluetooth

struct CameraSelectionView: View {
    @ObservedObject var scanner = CentralManager()
    @State private var peripheral: Peripheral?
    @State private var showCameraView = false
    var body: some View {
        NavigationView {
            VStack {
                NavigationLink(destination: CameraView(peripheral: peripheral), isActive: $showCameraView) { EmptyView() }
                List {
                    ForEach(scanner.peripherals, id: \.self) { peripheral in
                        ZStack {
                            HStack() {
                                Text(peripheral.name)
                                Spacer()
                                Image(systemName: "chevron.right")
                                    .renderingMode(.template)
                                    .foregroundColor(.gray)
                            }
                            Button(action: {
                                NSLog("Connecting to \(peripheral.name)..")
                                peripheral.connect { error in
                                    if error != nil {
                                        NSLog("Error connecting to \(peripheral.name)")
                                        return
                                    }
                                    NSLog("Connected to \(peripheral.name)!")
                                    showCameraView = true
                                    self.peripheral = peripheral
                                }
                            }, label: {
                                EmptyView()
                            })
                        }
                    }
                }
            }
            .onAppear {
                if let peripheral = peripheral {
                    NSLog("Disconnecting to \(peripheral.name)..")
                    peripheral.disconnect()
                }
                NSLog("Scanning for GoPro cameras..")
                scanner.start(withServices: [CBUUID(string: "FEA6")])
            }
            .onDisappear { scanner.stop() }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text("Select Camera").fontWeight(.bold)
                }
            }
        }
        .navigationViewStyle(StackNavigationViewStyle())
    }
}

struct CameraSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        CameraSelectionView()
    }
}
