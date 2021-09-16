:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

============
Contributing
============

Contributions are welcome, are greatly appreciated, and credit will always be given.

You can contribute in many ways:

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

#. Fork the Open GoPro repo on GitHub.
#. Clone your fork locally:

    .. code-block:: console

        $ git clone git@github.com:your_name_here/OpenGoPro.git

#. Enter the sdk_wireless_camera_control directory:

    .. code-block:: console

        $ cd OpenGoPro/demos/python/sdk_wireless_camera_control

#. Install your local copy into a virtual environment. The activation directory may vary based on your OS

    .. code-block:: console

        $ python -m venv venv
        $ source ./venv/bin/activate
        $ pip install -r requirements-dev.txt -r requirements.txt

4. Create a branch for local development, originating from the `main` branch:

    .. code-block:: console

        $ git checkout -b name-of-your-bugfix-or-feature main

5. Make your changes locally. When you're done making changes, check that your changes pass pylint and the unit tests:

    .. code-block:: console

        $ make format lint unit_tests

6. Commit your changes and push your branch to GitHub:

    .. code-block:: console

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated.
2. Modify the ``CHANGELOG.rst``.
3. The pull request should work for Python 3.8.x on the following platforms:
    - Windows 10, version 16299 (Fall Creators Update) and greater
    - Linux distributions with BlueZ >= 5.43
    - OS X / macOS >= 10.11
4. Squash all your commits on your PR branch, if the commits are not solving
    different problems and you are committing them in the same PR. In that case,
    consider making several PRs instead.
5. Feel free to add your name as a contributor to the ``AUTHORS.rst`` file!