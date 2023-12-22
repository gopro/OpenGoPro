# Open GoPro Developer README

Current Version: 2.0

<img src="docs/assets/images/logos/logo.png" alt="GoPro Logo" style="width: 35%;"/>

This README is for a developer who wants to modify or contribute to this repo. If you are a user (i.e.
you don't want to make changes to this repo), see the Open GoPro [Github Pages site](https://gopro.github.io/OpenGoPro/). If you
are just looking for demos, you can browse the `demos` folder here.

## Overview

This repo consists of three types of content:

-   demos
-   documentation

## Demos

Demos are runnable examples in various languages / frameworks and can be found in the `demos` folder. Demos exist,
from their own perspective, independent to the Jekyll-based documentation described below. To create a demo,
follow the "Contributing" section of the [README](demos/README.md) in the `demos` folder.

## Documentation

The documentation can be found in the `docs` directory in markdown files. It is built as a [Jekyll](https://jekyllrb.com/)
static site and hosted via [Github Pages](https://pages.github.com/). For local deployment and other usage information,
see the `docs` folder [README](docs/README.md).


## Copyright

All relevant source files shall contain a copyright. This is managed via the "Pre Merge Checks" Github Action.
When a pull request is opened (or updated), this action will search for any missing / incorrect copyrights,
add / fix them, and update the branch. If for some reason this needs to be done manually, it can be done via:

```
make copyright
```

A file can be excluded from this process by adding the following in a comment on the first line:

`No (C) Copyright`
