# General

- Abstract more commands into features

# Platform support

- iOS not tested beyond minimal BLE testing. Need Wifi "driver"
- desktop hasn't even been considered yet.

# Database

- Use real one-to-many instead of certificate serialization hack

# Robustness

- Wifi Connections are taking a long time
- BLE can not communicate after waking up GoPro. Seems to be Hero13 only.
- Handle WiFi disconnects. How to get the SSID?
- Reconnect after BLE / WIFI disconnects
- Check statuses and retry in BLE code
- COHN querying and access point overlap might be messing up the camera

# Documentation

- Move to Dokka 2
- Create devops task to selectively uninternalize protobuf enums

# Testing

- AndroidInstrumentedTesting Koin setup is not working

# Demo App

- 10.5.5.9 RTSP stream viewer not working