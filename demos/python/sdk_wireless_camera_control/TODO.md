
# TODO

## General

-   [ ] Refactor commands / parsers so that setting / status parsers (i.e. enums) can be accessed from class, not instance
    -  This is already done for commands but needs to be for others
-   [ ] Better handle kwargs that match base dict args in command as_dict methods
-   [ ] More test coverage
-   [ ] Clean up artifacts after testing. Or use temp directory.
-   [ ] Make scalable for multiple simultaneous cameras
-   [ ] Allow encoding = False for Set Livestream Mode. Requires tracking livestream state to not pend on encoding started after sending Set Shutter On

## Documentation

-   [ ] Figure out autodoc type alias in `conf.py`
-   [ ] Make graphviz requirement optional for local builds

## GUI

-   [ ] refactoring / cleanup to more closely follow MVC
-   [ ] handle option and sequence params
-   [ ] Add support for complex JSON responses (i.e. media list)
-   [ ] Implement BLE tab
-   [ ] Allow lazy evaluation of message list and map in model

## BLE

-   [ ] Add services view to GattDB
-   [ ] Make bleak wrapper write with / without response configurable
-   [ ] Add option to read values during service discovery

## WiFi

-   [ ] Investigate MacOS delay after connecting WiFi
-   [ ] More Linux testing
-   [ ] Use descriptors for main driver access to OS-driver implementation
-   [ ] Move to program language (C?) instead of EN-US


