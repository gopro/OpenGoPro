#!/usr/bin/env bash
# build_protos.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jul  6 19:59:53 UTC 2022


CWD=$(pwd)
PROTO_SRC_DIR=$CWD/../../../protobuf
PROTO_OUT_DIR=$CWD/open_gopro/proto

# Clean all current protobuf files and stubs
rm -f $PROTO_OUT_DIR/*pb2.py* >/dev/null 2>&1

echo
echo "Building protobuf python files and stubs from .proto source files..."
pushd $PROTO_SRC_DIR
protoc --include_imports --descriptor_set_out=$CWD/descriptors --python_out=$PROTO_OUT_DIR --mypy_out=$PROTO_OUT_DIR *
popd

echo
echo "Converting relative imports to absolute..."
poetry run protol -o ./open_gopro/proto/ --in-place raw descriptors
rm descriptors

# Format generated files
echo
echo "Formatting..."
poetry run black open_gopro/proto
