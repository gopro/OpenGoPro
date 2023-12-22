
# TODO

## General

-   [ ] Generate BLE and HTTP API from specs (OpenAPI, protobuf, etc.)
-   [ ] Better handle kwargs that match base dict args in command as_dict methods
-   [ ] More test coverage
-   [ ] Clean up artifacts after testing. Or use temp directory.
-   [ ] Make scalable for multiple simultaneous cameras
-   [ ] Allow encoding = False for Set Livestream Mode. Requires tracking livestream state to not pend on encoding started after sending Set Shutter On
-   [ ] Add textual TUI

## Documentation

-   [ ] Figure out autodoc type alias in `conf.py`
-   [ ] Make graphviz requirement optional for local builds

## BLE

-   [ ] Add services view to GattDB
-   [ ] Make bleak wrapper write with / without response configurable
-   [ ] Add option to read values during service discovery

## WiFi

-   [ ] Investigate MacOS delay after connecting WiFi
-   [ ] More Linux testing
-   [ ] Use descriptors for main driver access to OS-driver implementation
-   [ ] Move to program language (C?) instead of EN-US


