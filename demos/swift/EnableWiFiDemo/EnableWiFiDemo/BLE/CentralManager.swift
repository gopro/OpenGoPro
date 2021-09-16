/* CentralManager.swift/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:07 PM */

//
//  CentralManager.swift
//  EnableWiFiDemo
//

import Foundation
import CoreBluetooth

/// A simple wrapper around CBCentralManager to handle CoreBluetooth Central related tasks
final class CentralManager: NSObject, ObservableObject {
    @Published var peripherals: [Peripheral] = []

    private var manager: CBCentralManager!
    private var isReady: Bool { get { return manager.state == .poweredOn } }
    @Atomic private var onCentralStateChange: ((CBManagerState) -> Void)?

    override init() {
        super.init()
        let queue = DispatchQueue(label: "com.gopro.ble.central.queue", qos: .default)
        manager = CBCentralManager(delegate: self, queue: queue)
    }

    /// Starts a new BLE scan
    /// - Parameter withServices: the service UUIDs to scan for
    func start(withServices: [CBUUID]) {
        if isReady {
            peripherals.removeAll()
            manager.scanForPeripherals(withServices: withServices, options: nil)
        } else {
            onCentralStateChange = { [weak self] state in
                if state == .poweredOn {
                    DispatchQueue.main.async {
                        self?.start(withServices: withServices)
                    }
                }
            }
        }
    }

    /// Stops the current scan
    func stop() {
        manager.stopScan()
    }

    /// Connects the peripheral
    /// - Parameter peripheral: The peripheral to be connected
    func connectPeripheral(_ peripheral: CBPeripheral) {
        manager.connect(peripheral, options: nil)
    }

    /// Disconnects the peripheral
    /// - Parameter peripheral: The peripheral to disconnect
    func disconnectPeripheral(_ peripheral: CBPeripheral) {
        manager.cancelPeripheralConnection(peripheral)
    }
}

extension CentralManager : CBCentralManagerDelegate {
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        onCentralStateChange?(central.state)
    }

    func centralManager(_ central: CBCentralManager, didDiscover cbPeripheral: CBPeripheral,
                        advertisementData: [String : Any], rssi RSSI: NSNumber) {
        guard let localName: String = advertisementData["kCBAdvDataLocalName"] as? String else { return }

        let peripheral = Peripheral(peripheral: cbPeripheral, localName: localName, manager: self)
        if peripherals.filter({$0.identifier == peripheral.identifier}).first == nil {
            DispatchQueue.main.async { [weak self] in
                self?.peripherals.append(peripheral)
            }
        }
    }

    func centralManager(_ central: CBCentralManager, didConnect cbPeripheral: CBPeripheral) {
        guard let peripheral = peripherals.filter({$0.identifier == cbPeripheral.identifier.uuidString}).first else { return }
        peripheral.onConnect?(nil)
    }

    func centralManager(_ central: CBCentralManager, didFailToConnect cbPeripheral: CBPeripheral, error: Error?) {
        guard let peripheral = peripherals.filter({$0.identifier == cbPeripheral.identifier.uuidString}).first,
              let error = error else { return }

        peripheral.onConnect?(error)

        DispatchQueue.main.async { [weak self] in
            let index = self?.peripherals.firstIndex(of: peripheral)
            self?.peripherals.remove(at: index!)
        }

    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral cbPeripheral: CBPeripheral, error: Error?) {
        guard let peripheral = peripherals.filter({$0.identifier == cbPeripheral.identifier.uuidString}).first else { return }

        peripheral.onDisconnect?(error)

        DispatchQueue.main.async { [weak self] in
            let index = self?.peripherals.firstIndex(of: peripheral)
            self?.peripherals.remove(at: index!)
        }
    }
}
