# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:25 PM

PROTO_BUILD_DIR=.build/protobuf/python/*
PYTHON_TUTORIAL_PROTO_DIR=demos/python/tutorial/tutorial_modules/tutorial_5_ble_protobuf/proto
PYTHON_SDK_PROTO_DIR=demos/python/sdk_wireless_camera_control/open_gopro/proto

.PHONY: protos
protos: ## Build generated code from protobuf files
	@docker compose run --build --rm proto-build
	@rm -rf ${PYTHON_TUTORIAL_PROTO_DIR}/*pb2.py* && mkdir -p ${PYTHON_TUTORIAL_PROTO_DIR}
	@cp ${PROTO_BUILD_DIR} ${PYTHON_TUTORIAL_PROTO_DIR}
	@rm -rf ${PYTHON_SDK_PROTO_DIR}/*pb2.py* && mkdir -p ${PYTHON_SDK_PROTO_DIR}
	@cp ${PROTO_BUILD_DIR} ${PYTHON_SDK_PROTO_DIR}
