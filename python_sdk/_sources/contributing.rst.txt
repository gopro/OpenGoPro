:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

============
Contributing
============

Contributions are welcome, are greatly appreciated, and credit will always be given.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/gopro/OpenGoPro/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Open GoPro could always use more documentation, whether as part of the
official Open GoPro docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/gopro/OpenGoPro/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Get Started!
------------

Ready to contribute? Here's how to set up Open GoPro for local development.

Minimal Requirements
~~~~~~~~~~~~~~~~~~~~

* Python (>= 3.9, < 3.12)
* `Poetry <https://python-poetry.org/docs/#installation>`_ : Needed to install dependencies / development tasks

Additional Optional Requirements:

* `protoc <https://grpc.io/docs/protoc-installation/>`_  to build protobuf python files from .proto's
* `graphviz <https://graphviz.org/>`_  to build diagrams in sphinx

Steps
~~~~~

#. Fork the Open GoPro repo on GitHub.
#. Clone your fork locally:

    .. code-block:: console

        $ git clone git@github.com:your_name_here/OpenGoPro.git

#. Enter the sdk_wireless_camera_control directory:

    .. code-block:: console

        $ cd OpenGoPro/demos/python/sdk_wireless_camera_control

#. Create a branch for local development, originating from the `main` branch:

    .. code-block:: console

        $ git checkout -b name-of-your-bugfix-or-feature main

#. Install your local copy into a virtual environment.

    .. code-block:: console

        $ poetry install --all-extras

#. Make your changes locally. When you're done making changes, check that your changes are:

    * formatted
    * pass type checking
    * pass linting
    * pass unit tests
    * pass docstring tests

    .. code-block:: console

        $ poetry run poe all

    Note that each of these checks can be run individually. For more information, see:

    .. code-block:: console

        $ poetry run poe --help

#. Commit your changes, push your branch to GitHub, and submit a pull request into `main`. Once the Pull Request is made,
   Github Actions will test the changes across multiple OS's and Python versions.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. If the pull request adds functionality, the docs should be updated. The docs can be build locally via:

    .. code-block:: console

        $ poetry run poe docs

#. Modify the ``CHANGELOG.rst``.
#. The pull request should work for Python 3.8 - 3.12 on the following platforms:

    - Windows 10, version 16299 (Fall Creators Update) and greater
    - Linux distributions with BlueZ >= 5.43
    - OS X / macOS >= 10.11

#. Feel free to add your name as a contributor to the ``AUTHORS.rst`` file!