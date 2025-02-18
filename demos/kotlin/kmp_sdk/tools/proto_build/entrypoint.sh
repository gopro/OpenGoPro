#!/usr/bin/env bash

PROTO_SRC_DIR=/proto_in

function build_python()
{
    rm -rf $PROTO_PYTHON_OUT_DIR && mkdir -p $PROTO_PYTHON_OUT_DIR
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

    # Format generated files
    echo
    echo "Formatting..."
    black .
    popd
}

function build_kotlin()
{
    echo "Building kotlin protobuf files using pbandk..."
    export PATH=$PATH:/
    rm -rf /proto_output_kotlin/*
    gosu user:user mkdir -p /home/user/temp
    # We can't run as root because pbank can't handle it: https://github.com/streem/pbandk/issues/73
    gosu user:user protoc --pbandk_out=kotlin_package=com.gopro.open_gopro.operations,visibility=internal:/home/user/temp -I $PROTO_SRC_DIR $PROTO_SRC_DIR/*
    mv /home/user/temp/com/gopro/open_gopro/entity/operation/* /proto_output_kotlin
}

# build_python
build_kotlin