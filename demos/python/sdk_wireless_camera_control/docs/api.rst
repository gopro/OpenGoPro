:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Interfaces
**********

This section is a reference for the Open GoPro Python Package API. The BLE / Wifi API's that
this package implements can be found in the Open GoPro documentation linked from :ref:`package summary<Summary>`

.. note::
   Not everything is exposed here. This section should only consist of the interface
   information that a user (not a developer) of the Open GoPro module should care about.

Also, for a higher-level summary / usage, see the :ref:`usage<Usage>` section

GoPro
=====

This can be imported as:

.. code-block:: python

   from open_gopro import GoPro

.. automodule:: open_gopro.gopro
   :members:

Responses
=========

This can be imported via:

.. code-block:: python

   from open_gopro import GoProResp

.. autoclass:: open_gopro.responses.GoProResp
   :members:

Constants
=========

These can be imported as:

.. code-block:: python

   from open_gopro import constants


.. automodule:: open_gopro.constants
   :members:
   :undoc-members:

API
===

This is both the base types that are used to implement the API (BLE Setting, Ble Status, etc). and the
version-specific API's themselves.

These should not be imported directly and instead should be accessed using the
api(:attr:`open_gopro.gopro.GoPro.api`) attribute of a GoPro(:class:`open_gopro.gopro.GoPro`) instance.

Base Types
----------

These are the base types that are used to implement version-specific API's.

BLE Setting
^^^^^^^^^^^

.. autoclass:: open_gopro.api.builders.BleSetting
   :members:

BLE Status
^^^^^^^^^^

.. autoclass:: open_gopro.api.builders.BleStatus
   :members:

WiFi Setting
^^^^^^^^^^^^

.. autoclass:: open_gopro.api.builders.WifiSetting
   :members:

API Version 1.0
---------------

BLE 1.0 Commands
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v1_0.ble_commands.BleCommandsV1_0
   :members:

BLE 1.0 Settings
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v1_0.ble_commands.BleSettingsV1_0
   :members:

BLE 1.0 Statuses
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v1_0.ble_commands.BleStatusesV1_0
   :members:

WiFi 1.0 Commands
^^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v1_0.wifi_commands.WifiCommandsV1_0
   :members:

WiFi 1.0 Settings
^^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v1_0.wifi_commands.WifiSettingsV1_0
   :members:

1.0 Parameters
^^^^^^^^^^^^^^

All of these parameters can be accessed via:

.. code-block:: python

   from open_gopro import params

.. autoclass:: open_gopro.api.v1_0.params.ParamsV1_0
   :members:
   :undoc-members:

API Version 2.0
---------------

BLE 2.0 Commands
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v2_0.ble_commands.BleCommandsV2_0
   :members:
   :inherited-members:

BLE 2.0 Settings
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v2_0.ble_commands.BleSettingsV2_0
   :members:
   :inherited-members:

BLE 2.0 Statuses
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v2_0.ble_commands.BleStatusesV2_0
   :members:
   :inherited-members:

WiFi 2.0 Commands
^^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v2_0.wifi_commands.WifiCommandsV2_0
   :members:
   :inherited-members:

WiFi 2.0 Settings
^^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.v2_0.wifi_commands.WifiSettingsV2_0
   :members:
   :inherited-members:

2.0 Parameters
^^^^^^^^^^^^^^

All of these parameters can be accessed via:

.. code-block:: python

   from open_gopro import params

.. autoclass:: open_gopro.api.v2_0.params.ParamsV2_0
   :members:
   :undoc-members:
   :inherited-members:
