#!/usr/bin/env bash

# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:54 UTC 2024

PROTO_SRC_DIR=/proto_in
PROTO_PYTHON_OUT_DIR=/proto_output/python
PROTO_KOTLIN_OUT_DIR=/proto_output/kotlin

function build_python() {
    rm -rf $PROTO_PYTHON_OUT_DIR/* && mkdir -p $PROTO_PYTHON_OUT_DIR
    echo
    echo "Building protobuf python files and stubs from .proto source files..."
    pushd $PROTO_SRC_DIR
    protoc --include_imports --descriptor_set_out=$PROTO_PYTHON_OUT_DIR/descriptors --python_out=$PROTO_PYTHON_OUT_DIR --mypy_out=$PROTO_PYTHON_OUT_DIR *
    popd

    pushd $PROTO_PYTHON_OUT_DIR
    echo
    echo "Converting relative imports to absolute..."
    protol -o . --in-place raw descriptors
    rm descriptors
}

function build_kotlin() {
    echo "Building kotlin protobuf files using pbandk..."
    export PATH=$PATH:/
    rm -rf $PROTO_KOTLIN_OUT_DIR/* && mkdir -p $PROTO_KOTLIN_OUT_DIR
    gosu user:user mkdir -p /home/user/temp
    # We can't run as root because pbank can't handle it: https://github.com/streem/pbandk/issues/73
    gosu user:user protoc --pbandk_out=kotlin_package=com.gopro.open_gopro.operations,visibility=internal:/home/user/temp -I $PROTO_SRC_DIR $PROTO_SRC_DIR/*
    mv /home/user/temp/com/gopro/open_gopro/operations/* $PROTO_KOTLIN_OUT_DIR
    set-kmp-scopes /kmp_manipulator_config.toml $PROTO_KOTLIN_OUT_DIR
}

build_python
build_kotlin

echo "Protobuf build complete!"
