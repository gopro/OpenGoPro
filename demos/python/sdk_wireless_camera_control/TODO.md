# TODO

-   [ ] Refactor commands / parsers so that setting / status parsers (i.e. enums) can be accessed from class, not instance
-   [ ] Clean up and align BLE and WiFi command / response logging and parsing
-   [ ] Figure out autodoc type alias in `conf.py`
-   [ ] dynamically set docstring override in conf.py for commands so the override isn't needed for each command definition
-   [ ] Fix BLE set preset API doc signature
-   [ ] Better handle kwargs that match base dict args in command as_dict methods
-   [ ] Investigate worthiness of move to asyncio
-   [ ] Add fastpass property to commands to control lock acquiring / release
-   [ ] Add services view to GattDB
-   [ ] Make bleak wrapper write with / without response configurable
-   [ ] Add option to read values during service discovery
-   [ ] GUI refactoring / cleanup to more closely follow MVC
-   [ ] Add comments to GUI
-   [ ] handle option and sequence params in GUI
-   [ ] Make scalable for multiple simultaneous cameras
-   [ ] Add USB support
-   [ ] Investigate MacOS delay after connecting WiFi
-   [ ] More test coverage
-   [ ] Clean up artifacts after testing

# Blocked

-   Remove command docstring redirection once [this](https://github.com/sphinx-doc/sphinx/issues/10193) is fixed
