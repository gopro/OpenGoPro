# Limitations / Known Issues

## Limitations

### Potential Device ID collisions

Since BLE scans contain only the last 4 digits of the serial number, it is possible for there to be multiple
devices with the same identifier. We could work around this by connecting BLE first to get the complete
serial number.
