# KMP Protobuf Manipulator

This is a small Python package to manipulate Kotlin code that has been generated from protobufs.

Currently its only job is to selectively change scopes from `internal` to `public`.

## Installation

Install via `pip install .`

## Usage

There is one script in the package `set-kmp-scopes`. It takes as input:

-   a directory of .kt files
-   a config file specify what scopes should be changed. See [kmp_manipulator_config.toml](../kmp_manipulator_config.toml)
    as an example.

Run it with `--help` for more input
