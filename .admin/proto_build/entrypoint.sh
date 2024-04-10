#!/usr/bin/env bash
# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:54 UTC 2024


PROTO_SRC_DIR=/proto_in
PROTO_PYTHON_OUT_DIR=/proto_python_out

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
