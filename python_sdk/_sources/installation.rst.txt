:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

============
Installation
============

Stable release
--------------

This is the preferred method to install Open GoPro, as it will always install the most recent stable release
from `PyPi <https://pypi.org/project/open-gopro/>`_ .

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Minimal Install
^^^^^^^^^^^^^^^

To minimally install Open GoPro (to use the library and CLI demos), run this command in your terminal:

.. code-block:: console

    $ pip install open-gopro

Additional GUI Install
^^^^^^^^^^^^^^^^^^^^^^

To additionally install the extra dependencies to run the GUI demos:

.. code-block:: console

    $ pip install open-gopro[gui]


External Dependencies
^^^^^^^^^^^^^^^^^^^^^

In order to use any of the Webcam API's, ensure first that your system is setup to
`Use the GoPro as a Webcam <https://community.gopro.com/s/article/GoPro-Webcam?language=de>`_


From sources
------------

The sources for Open GoPro can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone https://github.com/gopro/OpenGoPro

Or download the `zip`_:

.. code-block:: console

    $ curl  -OL https://github.com/gopro/OpenGoPro/archive/refs/heads/main.zip

Once you have a copy of the source, you can install it:

First, enter the directory where the source code exists

.. code-block:: console

    $ cd OpenGoPro/demos/python/sdk_wireless_camera_control

Then install the package

.. code-block:: console

    $ pip install .

.. _Github repo: https://github.com/gopro/OpenGoPro
.. _zip: https://github.com/gopro/OpenGoPro/archive/refs/heads/main.zip

For Developers
^^^^^^^^^^^^^^

The above installation will not install Open GoPro in editable mode. If you want to modify the package so that
you can change it, for i.e. development, see :ref:`Contribution<Steps>`.
