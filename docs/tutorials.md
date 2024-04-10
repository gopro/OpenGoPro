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
[supported camera](/ble/index.html#supported-cameras).
They will provide walk-throughs and sample code to use the relevant language / framework to exercise the
Open GoPro Interface using Bluetooth Low Energy (BLE) and HTTP over WiFi.

{% warning %}
The tutorials are only tested on the latest camera / firmware combination. This is only an issue in cases where
capabilities change between cameras such as setting options.
{% endwarning %}

The tutorials are meant as an introduction to the Open GoPro specification. They are not a substitute
for the complete [BLE](/ble/index.html) and [HTTP](/http)
specifications which will be your main source of reference after completing the tutorials.

{% for tutorial in site.tutorials %}

-   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }})
    {% endfor %}
