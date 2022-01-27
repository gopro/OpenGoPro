---
title: 'HTTP Specifications'
permalink: /http
---

This page will provide links to each version of the Open GoPro HTTP specification, as well
as an overview of the changes from the previous version.
Click on an individual spec to see its complete information including possible commands, settings, etc.

{% note Since the Open GoPro API varies based on the version, it is necessary to query the Open GoPro version
using the Get Version command upon connection %}

# Versions

## [HTTP Specification 2.0](http_versions/http_2_0.md)

-   Hilights:
    -   Capture media
    -   Track camera state
    -   Get media list and download files / metadata
    -   Load / edit presets
    -   Configure and use as webcam
    -   Add / remove hilights
-   Breaking changes:
    -   Settings endpoint has changed to: `gopro/camera/setting?setting={setting}&option={option}`
        See the [quick reference]({% link specs/http_versions/http_2_0.md %}#settings-quick-reference) for more information
    -   Video Digital Lens setting parameter changes:
        -   Narrow changed from 6 to 2
    -   Photo Digital Lens setting parameter changes:
        -   Wide changed from 22 to 101
        -   Linear changed from 23 to 102
        -   Narrow changed from 24 to 19
        -   Max Superview changed from 25 to 100
    -   Multishot Digital Lens parameter changes:
        -   Wide changed from 2 to 101
        -   Narrow changed from 24 to 19

## [HTTP Specification 1.0](http_versions/http_1_0.md)

-   Initial API
