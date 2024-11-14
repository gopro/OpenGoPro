# Platform support

- [ ] iOS not tested. Need Wifi "driver"
- [ ] desktop hasn't even been considered yet.

# UI

- [ ]  Stream viewer not working. Needs massive exoplayer investigation.

# Database

- [ ] User real one-to-many instead of certificate serialization hack

# Robustness 

- [ ] Handle WiFi disconnects. How to get the SSID?
- [ ] Handle BLE disconnects. It seems I'm not getting the events from Kable?
- [ ] Reconnect after BLE / WIFI disconnects

# Documentation

- [ ] Move to Dokka 2
- [ ] Create devops task to selectively uninternalize protobuf enums