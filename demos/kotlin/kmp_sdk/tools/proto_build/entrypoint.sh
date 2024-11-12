#!/usr/bin/env bash

PROTO_SRC_DIR=/proto_in
PROTO_PYTHON_OUT_DIR=/proto_output/python
PROTO_KOTLIN_OUT_DIR=/proto_output/kotlin

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
    rm -rf $PROTO_KOTLIN_OUT_DIR/*
    # We can't run as root because pbank can't handle it: https://github.com/streem/pbandk/issues/73
    # TODO do we want these to be internal or public?
    # gosu user:user protoc --pbandk_out=visibility=internal:$PROTO_KOTLIN_OUT_DIR -I $PROTO_SRC_DIR $PROTO_SRC_DIR/*
    gosu user:user protoc --pbandk_out=$PROTO_KOTLIN_OUT_DIR -I $PROTO_SRC_DIR $PROTO_SRC_DIR/*
}

# build_python
build_kotlin