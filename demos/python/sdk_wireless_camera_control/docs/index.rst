:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Open GoPro Python SDK
=====================

.. figure:: https://raw.githubusercontent.com/gopro/OpenGoPro/main/docs/assets/images/logos/logo.png
    :alt: GoPro Logo
    :width: 50%

.. image:: https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_test.yml/badge.svg
    :target: https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_test.yml
    :alt: Build and Test

.. image:: https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_deploy_docs.yml/badge.svg
    :target: https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_deploy_docs.yml
    :alt: Build and Test

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

Summary
-------

Welcome to the Open GoPro Python package documentation. This is a Python package that provides an
interface for the user to exercise the Open GoPro Bluetooth Low Energy (BLE) and Wi-Fi API's.

This package implements the API as defined in the `Open GoPro Specification <https://github.com/gopro/OpenGoPro>`_ .

For more information on the API, see the relevant documentation:

* `BLE API <https://github.com/gopro/OpenGoPro/tree/main/docs/ble>`_
* `Wi-Fi API <https://github.com/gopro/OpenGoPro/tree/main/docs/wifi>`_


Features
--------

- Top-level GoPro class interface to use both BLE / WiFi
- Cross-platform (tested on MacOS Big Sur, Windows 10, and Ubuntu 20.04)
    - BLE implemented using `bleak <https://pypi.org/project/bleak/>`_
    - Wi-Fi controller provided in the Open GoPro package (loosely based on the `Wireless Library <https://pypi.org/project/wireless/>`_ )
- Supports all `Open GoPro API's <https://github.com/gopro/OpenGoPro>`_
- Automatically handles some required functionality:
    - manage camera ready / encoding
    - periodically sends keep alive signals
- Includes demo scripts installed as command-line applications to show BLE and WiFi functionality


.. toctree::
    :maxdepth: 4
    :caption: Contents:

    installation
    quickstart
    usage
    api
    troubleshooting
    contributing
    authors
    changelog
    future_work
