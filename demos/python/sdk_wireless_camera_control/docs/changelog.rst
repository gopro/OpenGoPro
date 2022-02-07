:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

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
