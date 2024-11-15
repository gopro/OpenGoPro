# General
- [ ] Abstract more commands into features
- [ ] Generate setting / status code

# Platform support

- [ ] iOS not tested. Need Wifi "driver"
- [ ] desktop hasn't even been considered yet.

# Database

- [ ] User real one-to-many instead of certificate serialization hack

# Robustness 

- [ ] Handle WiFi disconnects. How to get the SSID?
- [ ] Handle BLE disconnects. It seems I'm not getting the events from Kable?
- [ ] Reconnect after BLE / WIFI disconnects
- [ ] Check statuses and retry in BLE code

# Documentation

- [ ] Move to Dokka 2
- [ ] Create devops task to selectively uninternalize protobuf enums