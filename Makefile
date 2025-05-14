# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:25 PM

VERSION:=2.0

PROTO_BUILD_DIR=.build/protobuf
PYTHON_TUTORIAL_PROTO_DIR=demos/python/tutorial/tutorial_modules/tutorial_5_ble_protobuf/proto
PYTHON_SDK_PROTO_DIR=demos/python/sdk_wireless_camera_control/open_gopro/models/proto
KOTLIN_SDK_PROTO_DIR=demos/kotlin/kmp_sdk/wsdk/src/commonMain/kotlin/com/gopro/open_gopro/entity/operation/proto

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: protos
protos: ## Build generated code from protobuf files
	@docker compose run --build --rm proto-build
	@rm -rf ${PYTHON_TUTORIAL_PROTO_DIR}/*pb2.py* && mkdir -p ${PYTHON_TUTORIAL_PROTO_DIR}
	@cp ${PROTO_BUILD_DIR}/python/* ${PYTHON_TUTORIAL_PROTO_DIR}
	@rm -rf ${PYTHON_SDK_PROTO_DIR}/*pb2.py* && mkdir -p ${PYTHON_SDK_PROTO_DIR}
	@cp ${PROTO_BUILD_DIR}/python/* ${PYTHON_SDK_PROTO_DIR}
	@rm -rf ${KOTLIN_SDK_PROTO_DIR}/* && mkdir -p ${KOTLIN_SDK_PROTO_DIR}
	@cp ${PROTO_BUILD_DIR}/kotlin/* ${KOTLIN_SDK_PROTO_DIR}

.PHONY: copyright
copyright: ## Check for and add missing copyrights
	@echo "©️ Verifying / adding copyrights..."
	@.admin/copyright -i . $(VERSION)