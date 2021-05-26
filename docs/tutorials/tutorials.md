---
permalink: /tutorials/
read_time: false
redirect_from:
    - /bash
    - /python
---

# Tutorials

There exists several walk-through tutorials in different languages / frameworks for getting started
with Open GoPro:

# Python

This set of tutorials is a series of sample python script and accompanying .html walk-throughs
to implement basic functionality to interact with a GoPro device using Python.

The tutorials will provide a walk-through to use Python to exercise the
Open GoPro Interface using [bleak](https://bleak.readthedocs.io/en/latest/api.html)
for Bluetooth Low Energy (BLE) and [requests](https://docs.python-requests.org/en/master/) for HTTP.

It is ok not to have read the [BLE]({% link specs/ble.md %}) or [WiFi]({% link specs/wifi.md %}) interface documentation first as we will describe it as needed here.
After completing the tutorials, you will need to reference it for future development.

{% for tutorial in site.python-tutorials %}
-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
{% endfor %}

{% note  These are extremely stripped down Python tutorials that are only meant to show the basics. %}
For a complete Python SDK that uses [bleak](https://bleak.readthedocs.io/en/latest/) as the backend as well as a
cross-platform WiFi backend to easily write Python apps that control the GoPro, see the [Open GoPro Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)

# Bash

BlueZ tutorial for Ubuntu using the command line:

{% for tutorial in site.bash-tutorials %}
-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
{% endfor %}

# More to come!
