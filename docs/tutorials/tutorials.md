---
permalink: /tutorials/
read_time: false
redirect_from:
    - /bash
    - /python
---

# Tutorials

Several walk-through tutorials in different languages / frameworks exist for getting started with Open GoPro.

# Python

This set of tutorials is a series of sample python scripts and accompanying .html walk-throughs
to implement basic functionality to interact with a GoPro device using Python.

The tutorials support Open GoPro Versions 1.0 and 2.0. They will provide a walk-through to use Python to exercise the
Open GoPro Interface using [bleak](https://bleak.readthedocs.io/en/latest/api.html)
for Bluetooth Low Energy (BLE) and [requests](https://docs.python-requests.org/en/master/) for HTTP.

These tutorials are meant as an introduction to the Open GoPro specification. There is complete documentation
available for [BLE]({% link specs/ble.md %}) and [HTTP]({% link specs/http.md %}) which will be the main
source of reference after completing the tutorials.

{% for tutorial in site.python-tutorials %}
-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
{% endfor %}

{% note These are stripped down Python tutorials that are only meant to show the basics. %}
For a complete Python SDK that uses [bleak](https://bleak.readthedocs.io/en/latest/) as the backend as well as a
cross-platform WiFi backend to easily write Python apps that control the GoPro, see the [Open GoPro Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)

# Bash

BlueZ tutorial for Ubuntu using the command line:

{% for tutorial in site.bash-tutorials %}
-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
{% endfor %}

# More to come!
