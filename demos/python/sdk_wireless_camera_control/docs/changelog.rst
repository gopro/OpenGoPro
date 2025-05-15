:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

<<<<<<< Updated upstream
=======
Unreleased
----------
* Add stream feature abstraction and update stream demos

0.20.0 (May-12-2025)
--------------------
* NOTE! This is a major update and includes breaking API changes
* Major refactor to support any combination of network interfaces for WirelessGoPro
* Add observable / observer base type and use for asynchronous push notification operations
* Maintain database of COHN credentials
* Remove Python 3.10 and add 3.13 support

>>>>>>> Stashed changes
0.19.8 (April-30-2025)
----------------------
* Default ainput printer arg to None to support non-terminal applications without access to stdout

0.19.7 (April-28-2025)
----------------------
* Add Reboot Command
* Hardcode bypass_eula_check to True to allow connecting to networks without internet access.
* Add scheduled capture setting (and support for other future quantitative settings)

0.19.6 (April-8-2025)
---------------------
* Update dependencies
* Fix register / unregister all settings / statuses

0.19.5 (March-27-2025)
----------------------
* Fix race condition in BLE opening
* Set third party when opening device
* Add more detailed advertisement data parsing capability
* Add 4:3 and 16:9 preset enums
* Use constant setting IDs when getting presets

0.19.4 (March-21-2025)
----------------------
* Inject BLE keep alive and set the default to 3 seconds
* Make WiFi connect and disconnect async methods

0.19.3 (March-20-2025)
----------------------
* Fix BLE Keep alive

0.19.2 (March-19-2025)
----------------------
* Allow more configurability in wifi open / close

0.19.1 (March-18-2025)
----------------------
* Add encode argument for set_livestream_mode

0.19.0 (February-20-2025)
-------------------------
* Major settings and status API changes to use auto-generated code

0.18.0 (January-7-2025)
-----------------------
* Change supported Python versions to >= 3.10 and < 3.13

0.17.1 (September-13-2024)
--------------------------
* Fix COHN demo
* Fix livestream demo CLI argument parsing
* Add `raw` field to MediaList object

0.17.0 (September-9-2024)
-------------------------
* Add Hero 13 support (settings, statuses, protobuf)
* Fix MacOS Wifi scanning
* Major infrastructure updates

0.16.2 (July-18-2024)
---------------------

* Add Setting 125
* Don't default to hardcoded parameters for set livestream mode
* Fix routing for Get All Setting / Status commands

0.16.1 (April-23-2024)
----------------------

* Always use extended headers
* Add Delete Media HTTP API's
* Add port argument to Preview Stream HTTP API
* Only ask for sudo password when required
* fix WiFi connection on RHEL based systems

0.16.0 (April-9-2024)
---------------------
* Refactor all network operations to operate on common Message class
* Add PUT Operation support
* Add Custom Preset Update
* Update Bleak to 0.21.1

0.15.1 (December-6-2023)
------------------------
* Fix livestream demo.

0.15.0 (December-6-2023)
------------------------
* Add alpha support for COHN (Camera-on-the-Home-Network)
    * A real implementation is going to require a major rearchitecture to dynamically add connection types.
* Remove TKinter GUI. Will be replaced with Textual TUI in the future
* Improve wifi SSID matching
* Fix unhashable pydantic base models

0.14.1 (September-21-2023)
--------------------------
* Fix BLE notifications not being routed correctly
* Don't hardcode media directory. Also append directory to filenames in media list.
* Fix malformed Set Setting HTTP url

0.14.0 (September-13-2023)
--------------------------
* NOTE! This is a major update and includes massive API breaking changes.
* Move to asyncio-based framework
* Add HERO 12 support
* Move from generic response to per-command typed response
* Improve video viewer latency
* Improve BLE and HTTP setting documentation
* Add media list and metadata pydantic models

0.13.0 (February-24-2023)
-------------------------

* Allow for GUI dependencies to be optional (with "gui" extras)
* Add English language verification for Wifi Driver
* Documentation fixes missed from 0.12.0
* Update dependencies (including bleak to 0.19.5)

0.12.0 (December-16-2023)
-------------------------
* Add USB support

    * Introduces breaking changes of top level interface (i.e. GoPro --> WirelessGoPro / WiredGoPro)
    * Includes mDNS discovery of GoPro's
* Add run-time python version verification
* Improve error messaging and documentation around wifi interface issues
* Add livestream demo
* Add webcam demo
* Add message rules for Commands / Settings / Statuses (Fastpass, etc)

0.11.2 (November-9-2022)
------------------------
* Update bleak to 0.19.0
* Improve Bluetooth Scan delays
* Add support for Hero 11 Mini

0.11.1 (October-18-2022)
------------------------
* Improve Mac Wifi connection robustness
* Fix BLE can ignoring timeout and retry args

0.11.0 (September-14-2022)
--------------------------
* Add Hero 11 Support
* Add Presets Control Demo
* Refactor all commands to be variadic
* Add API GUI MVC framework
* Protobuf command bug fixes
* Improve API doc generation and docstring verification
* Drop Python 3.8 support

0.10.0 (July-14-2022)
---------------------
* Add sudo password argument to Wifi Controller and expose through CLI demos via stdin
* Add more protobuf commands and missing protobuf ID parsing functionality
* Add livestream demo GUI
* Change preview stream demo to be a GUI
* Add support for fragmenting long data packets when sending BLE data

0.9.2 (June-16-2022)
-----------------------
* Remove use of importlib.metadata as it was complicating pyinstaller use of this package

0.9.1 (May-27-2022)
-----------------------
* Improve non-main thread and asyncio exception handling
* Add pydocstyle verification

0.9.0 (February-7-2022)
-----------------------
* Move to Poetry-based development environment
* Fix docstring inconsistencies

0.8.0 (February-3-2022)
-----------------------
* Improve BLE connection Robustness
* Deprecate support for Open GoPro Versions other than 2.0
* Add set / date time commands
* Implement remaining protobuf commands and fix protobuf parsing
* Add hilight commands
* Implement common UUID type
* Add video performance mode
* Remove deprecated status and setting ID's

0.7.2 (January-3-2022)
----------------------
* Allow for WiFi adapter to specify interface
* Clean up Wifi adapter
* Bump test package versions

0.7.1 (December-16-2021)
-------------------------
* Add global behaviors commands and camera control status
* Add register / unregister all for settings and statuses
* Add max lens setting
* Improve API documentation

0.7.0 (October-27-2021)
-------------------------
* Add video performance mode functionality

0.6.3 (October-7-2021)
-------------------------
* Decouple response accumulating from parsing

0.6.2 (September-28-2021)
-------------------------
* Fix setup.py entrypoints for demo programs

0.6.1 (September-20-2021)
-------------------------

* make parsers available at instantiation
* use GoPro specific enums to handle invalid parameter cases
* handle HTTP GET errors
* add Construct typing
* update Construct parsers to return actual enum's so identity checks can be used

0.6.0 (September-2-2021)
------------------------

* Major refactor to support multiple Open GoPro API versions and different BLE / WiFi adapters
* Improve BLE connection robustness by ensuring disconnects
* Implement Open GoPro Version 2.0
* Major documentation updates
* Add end-to-end testing and improve test coverage
* Upgrade bleak
* Add connect WiFi demos

0.5.8 (August-10-2021)
----------------------

* Add option to start GoPro communication without WiFi (i.e only use BLE)
* Add battery logging example

0.5.7 (June-7-2021)
-------------------

* Fix wifi driver for Windows

0.5.6 (May-26-2021)
-------------------

* Minor documentation updates

0.5.5 (May-26-2021)
-------------------

* Documentation link updates

0.5.4 (May-6-2021)
------------------

* Update documentation to coexist with jekyll on Github pages

0.5.3 (April-15-2021)
---------------------

* Documentation updates
* Move into Open GoPro repo

0.5.2 (April-2-2021)
--------------------

* Add entrypoints for video, photo, and stream
* Updates to response interface for usability
* Fix Ubuntu Wifi driver scanning

0.5.1 (April-1-2021)
--------------------

* Add photo, video, and stream entry points
* Change active accumulating response to a dict indexed by UUID's to handle simultaneous active responses

0.5.0 (March-30-2021)
---------------------

* Add support for Ubuntu 20.04
* Upgrade to bleak 0.11.0

0.4.6 (March-29-2021)
---------------------

* Fix bug where multiple simultaneous sync responses weren't handled

0.4.5 (March-29-2021)
---------------------

* Infrastructure updates:
    - Move from flake8 to pylint in order to catch missing args in docstrings
    - Implement a lot of pylint suggestions

0.4.4 (March-27-2021)
---------------------

* Infrastructure updates:
    - Add Github actions for CI / CD
    - Fix all mypy and flake8 errors

0.4.3 (March-26-2021)
---------------------

* Make BLE interface controller-agnostic

0.4.2 (March-25-2021)
---------------------

* Fix line endings that were causing PyPi failures

0.4.1 (March-25-2021)
---------------------

* Fix install error by adding protobuf requirement

0.4.0 (March-25-2021)
---------------------

* Merge BLE and WiFi classes into one GoPro class
* Automatically periodically send keep alive
* Run pydocstyle on docstrings

0.3.3 (March-22-2021)
---------------------

* Add support to wait for encoding and system ready statuses in BLE
* Add protobuf framework (not being sent yet)
* Fix Wi-Fi SSID corner cases

0.3.2 (March-15-2021)
---------------------

* Handle case where BLE parameter has length 0
* Doc updates

0.3.1 (March-12-2021)
---------------------

* Add automatic VLC opening

0.3.0 (March-11-2021)
---------------------

* Wrote documentation and did some refactoring

0.2.0 (March-10-2021)
---------------------

* first usable Beta package.
* Should work on Windows and Mac

0.1.x (March-10-2021)
---------------------

* open_gopro created. Incremental updates until the package could actually install
