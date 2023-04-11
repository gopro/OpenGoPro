---
permalink: /tutorials/
read_time: false
---

# Tutorials

This set of tutorials is a series of sample scripts / files and accompanying .html walk-throughs
to implement basic functionality to interact with a GoPro device using the following languages:
- Python
- Kotlin
- More to come!

The tutorials only support Open GoPro Version 2.0 and must be run on a
[supported camera]({% link specs/ble_versions/ble_2_0.md %}#supported-cameras).
They will provide walk-throughs and sample code to use the relevant language / framework to exercise the
Open GoPro Interface using Bluetooth Low Energy (BLE) and HTTP over WiFi.

The tutorials are meant as an introduction to the Open GoPro specification. They are not a substitute
for the complete [BLE]({% link specs/ble_versions/ble_2_0.md %}) and [HTTP]({% link specs/http_versions/http_2_0.md %})
specifications which will be your main source of reference after completing the tutorials.

{% for tutorial in site.tutorials %}

-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
    {% endfor %}
