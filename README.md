# Open GoPro Developer README

Current Version: 2.0

<img src="https://raw.githubusercontent.com/gopro/OpenGoPro/gh-pages/assets/images/logos/logo.png" alt="GoPro Logo" style="width: 35%;"/>

This README is only for a developer who wants to modify or contribute to this repo. If you are a user (i.e.
you don't want to make changes to this repo), see the Open GoPro [Github Pages site](https://gopro.github.io/OpenGoPro/)
for specs and getting started with Open GoPro.

If you are just looking for demos, you can browse the `demos` folder here.

If you are looking for the [Python SDK](https://pypi.org/project/open_gopro/),
see its [documentation](https://gopro.github.io/OpenGoPro/python_sdk/).

## Overview

This repo consists of the following types of content:

## Demos

Demos are runnable examples in various languages / frameworks and can be found in the `demos` folder. Demos exist,
from their own perspective, independent to the Jekyll-based documentation described below. To create a demo,
follow the "Contributing" section of the [README](demos/README.md) in the `demos` folder.

## Capabilities

These are various specifications to describe specific camera / firmware version capabilities. For more information,
see the [BLE](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-capabilities) or
[HTTP](https://gopro.github.io/OpenGoPro/http#tag/settings) spec.

## Tools

These are utilities to perform various functionality needed by demos or tutorials. See the README of each tool
directory for more information.

## Copyright

All relevant source files shall contain a copyright. This is managed via the "Pre Merge Checks" Github Action.
When a pull request is opened (or updated), this action will search for any missing / incorrect copyrights,
add / fix them, and update the branch. If for some reason this needs to be done manually, it can be done via:

```
make copyright
```

A file can be excluded from this process by adding the following in a comment on the first line:

`No (C) Copyright`
