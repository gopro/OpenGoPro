# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:25 PM

ORIGINAL_VERSION=$(strip $$(awk '/Current Version: /{print $$NF}' README.md))
VERSION:=$(ORIGINAL_VERSION)

# See the following for explanation abou the site / base URL dance when building / serving / testing site
# https://mademistakes.com/mastering-jekyll/site-url-baseurl/#jekyll-development-and-siteurl
# Default URL's for building public site. Will be overwritten when building staging site
BUILD_HOST_URL:="https://gopro.github.io"
BUILD_BASE_URL:="/OpenGoPro"

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Docker images are currently not public. So we build if pull fails for the local use case.
.PHONY: docker-setup
docker-setup:
	-@docker compose pull jekyll plant-uml || docker compose build jekyll plant-uml

.PHONY: docker-kill
docker-kill:
	-@docker kill jekyll plant-uml > /dev/null 2>&1

.PHONY: clean
clean: ## Clean cached jekyll files
	@echo "🧼 Cleaning jekyll artifacts..."
	-@docker compose down > /dev/null 2>&1
	@rm -rf docs/_site docs/.jekyll-cache docs/.jekyll-metadata

.PHONY: serve
serve: docker-kill docker-setup
serve: ## Serve site locally
	@echo COMMAND="-u http://localhost:4998/ -b \"\" -p 4998 serve" > .env
	@docker compose up
	@rm -rf .env

.PHONY: build
build: docker-setup
build: ## Build site for deployment
	@echo COMMAND=\"-u ${BUILD_HOST_URL} -b ${BUILD_BASE_URL} build\" > .env
	@docker compose up --abort-on-container-exit
	@rm -rf .env

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

.PHONY: tests
tests: docker-setup clean
tests: ## Serve, then run link checker. Times out after 5 minutes.
	-@docker compose pull linkchecker || docker compose build linkchecker
	@echo COMMAND="-u http://jekyll:4998/ -b \"\" -p 4998 serve" > .env
	@docker compose --profile test up --abort-on-container-exit
	@rm -rf .env

.PHONY: copyright
copyright: ## Check for and add missing copyrights
	@echo "©️ Verifying / adding copyrights..."
	@.admin/copyright -i . $(ORIGINAL_VERSION)
