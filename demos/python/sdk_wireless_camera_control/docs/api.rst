:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Interfaces
==========

This section is a reference for the Open GoPro Python Package API. The BLE / Wifi API's that
this package implements can be found in the Open GoPro documentatino linked from :ref:`package summary<Summary>`

.. note::
   Not everything is exposed here. This section should only consist of the interface
   information that a user (not a developer) of the Open GoPro module should care about.

Also, for a higher-level summary / usage, see the :ref:`usage<Usage>` section

GoPro
-----

This can be imported as:

.. code-block:: python

   from open_gopro import GoPro

.. automodule:: open_gopro.gopro
   :members:

Commands (BLE)
**************

.. autoclass:: open_gopro.ble_commands.BleCommands
   :members:

Settings (BLE)
**************

.. autoclass:: open_gopro.ble_commands.BleSettings
   :members:

.. autoclass:: open_gopro.ble_commands.Setting
   :members:

Statuses (BLE)
**************

.. autoclass:: open_gopro.ble_commands.BleStatuses
   :members:

.. autoclass:: open_gopro.ble_commands.Status
   :members:

Commands (WiFi)
***************

.. autoclass:: open_gopro.wifi_commands.WifiCommands
   :members:

Settings (Wifi)
***************

.. autoclass:: open_gopro.wifi_commands.WifiSettings
   :members:

.. autoclass:: open_gopro.wifi_commands.Setting
   :members:

Responses
---------

This can be imported as:

.. code-block:: python

   from open_gopro import GoProResp

.. automodule:: open_gopro.responses
   :members:

Constants
---------

These can be imported as:

.. code-block:: python

   from open_gopro import constants


.. automodule:: open_gopro.constants
   :members:
   :undoc-members:

Parameters
----------

All of these parameters can be accessed via:

.. code-block:: python

   from open_gopro import params

.. automodule:: open_gopro.params
   :members:
   :undoc-members:

.. automodule:: open_gopro.params.params
   :members:
   :undoc-members: