# Open GoPro Developer README

[![Pre Merge Checks](https://github.com/gopro/OpenGoPro/actions/workflows/pre_merge_checks.yml/badge.svg)](https://github.com/gopro/OpenGoPro/actions/workflows/pre_merge_checks.yml)

This README is for a developer who wants to modify or contribute to this repo. If you are a user (i.e.
you don't want to make changes to this repo), see the [User README](README.md)

## Directory Structure

Any subdirectories will contain `README.md`'s with more information

```
├── .github
│   └── workflows: Github action definitions for CI / CD
├── .nojekyll: Required to prevent Github pages from overwriting custom CSS
├── _config.yml: Github pages configuration file
├── demos: complete demos to illustrate Open GoPro functionality
│   ├── ...
├── docker-compose.yml: Docker container definitions
├── Dockerfile: Docker image build steps
├── docs: Open GoPro interface Documentation
│   ├── assets
│   ├── ble: Bluetooth Low Energy documentation
│   ├── protobuf: protobuf descriptions
│   └── wifi: WiFi documentation
├── LICENSE
├── logo.png: GoPro logo used in many places throughout this repo
├── Makefile: top-level Makefile to abstract setup, building, etc.
├── README-dev.md: This file (README for a contributor to this repo)
├── README.md: Top level README for an Open GoPro user
├── README.html: generated html from README.md
├── tools
│   ├── hooks: Git hooks to be installed for development
│   └── rdocs: framework to build tutorials from .Rmd files
└── tutorials: walk-through guides to get started with the Open GoPro interface
    ├── ...
```

## Contribution Overview

1. Setup the repo for development using the Setup section below
1. Create a Pull Request of your changes on the [Open GoPro repo](https://github.com/gopro/OpenGoPro)

## Setup

At minimum, the git hooks need to be installed via:

```
make setup_hooks
```

If you plan to use the docker image (for example to update the tutorials), it must first be built with:

```
make setup_docker
```

All of the above can be done simultaneously with:

```
make setup
```

## Makefile

For more information on the Makefile goals, do:

```
make help
```

## Versioning

The version listed in the [README](README.md) is the single source of versioning. Therefore, to update the
version, update the "Current Version" there. This will be propagated to all of the copyright headers when
the commit is made.

> Note! Only update the version number. It is important for "Current Version " to remain as this is used for parsing