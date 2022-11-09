:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Open GoPro Python SDK
=====================

.. figure:: https://raw.githubusercontent.com/gopro/OpenGoPro/main/docs/assets/images/logos/logo.png
    :alt: GoPro Logo
    :width: 50%

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: MIT License

.. image:: https://img.shields.io/github/workflow/status/gopro/OpenGoPro/Python%20SDK%20Testing?label=Build%20and%20Test
    :target: https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_test.yml
    :alt: Build and Test

.. image:: https://img.shields.io/pypi/v/open-gopro
    :target: https://pypi.org/project/open-gopro/
    :alt: PyPI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

.. image:: _static/coverage.svg
    :alt: Coverage

Summary
-------

Welcome to the Open GoPro Python package documentation. This is a Python package that provides an
interface for the user to exercise the Open GoPro Bluetooth Low Energy (BLE) and Wi-Fi API's.

This package implements the API as defined in the `Open GoPro Specification <https://gopro.github.io/OpenGoPro/>`_ .
For more information on the API, see the relevant documentation:

- `BLE API <https://gopro.github.io/OpenGoPro/ble>`_
- `Wi-Fi API <https://gopro.github.io/OpenGoPro/http>`_

.. warning::
    This package requires Python >= version 3.9 and <= 3.10

Features
--------

- Top-level GoPro class interface to use both BLE / WiFi
- Cross-platform (tested on Windows 10, and Ubuntu 20.04, and >= MacOS Big Sur)

  - BLE controller implemented using `bleak <https://pypi.org/project/bleak/>`_
  - Wi-Fi controller provided in the Open GoPro package (loosely based on the `Wireless Library <https://pypi.org/project/wireless/>`_ )
- Supports all wireless commands, settings, and statuses from the `Open GoPro API <https://gopro.github.io/OpenGoPro/>`_
- Automatically handles connection maintenance:

  - manage camera ready / encoding
  - periodically sends keep alive signals
- Includes detailed logging for each module
- Includes demo scripts installed as command-line applications to show BLE and WiFi functionality such as:

  - Take a photo
  - GUI to send all commands and view the live / preview stream
  - Take a video
  - Log the battery

Getting Started
---------------

Here is a suggested procedure for getting acquainted with this package (it is the same as reading through
this document in order):

#. :ref:`Install<Installation>` the package
#. Try some of the :ref:`demos<QuickStart Guide>`
#. Implement your own example, perhaps starting with a demo, with :ref:`usage<Usage>` information
#. If you need more detailed implementation reference, see the Interface :ref:`documentation<Interfaces>`

Development
-----------

#. Set up the :ref:`development environment<Get Started!>`
#. Open a :ref:`Pull Request<Pull Request Guidelines>`

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
