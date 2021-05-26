# Swift Enable WiFi Demo

This demo demonstrates how to discover and connect to a GoPro camera via Bluetooth LE (BLE). Once a connection is
established, the demo demonstrates how to enable Wi-Fi on the GoPro camera and join the camera's Wi-Fi. The steps
required to join camera's Wi-Fi are:

1. Enable Wi-Fi
2. Request camera's Wi-Fi settings (SSID and password)
3. Use [iOS NetworkExtension](https://developer.apple.com/documentation/networkextension/nehotspotconfigurationmanager) API to join camera's WiFi

# Requirements

GoPro camera must be paired with the mobile device. If the camera is not paired, put the camera in pairing mode

# File Structure

## BLE

-   _CentralManager.swift_ - A simple wrapper around CBCentralManager to handle CoreBluetooth Central related tasks
-   _Peripheral.swift_ - A simple wrapper around CBPeripheral to handle CoreBluetooth Peripheral related tasks
-   _Peripheral+Camera.swift_ - An extension of Peripheral class for sending commands to a GoPro camera

## Views

-   _CameraSelectionView.swift_ - A SwiftUI list view for showing the nearby GoPro cameras
-   _CameraView.swift_ - A simple view with a button for initiate the request to enable Wi-Fi on the connected GoPro camera
