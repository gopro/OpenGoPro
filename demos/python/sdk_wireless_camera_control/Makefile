# Makefile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:30 AM

# This must be run from the directory it exists in.

OPEN_GO_PRO_DIR		:=
PACKAGE_DIR			:= open_gopro
DOCS_DIR			:= docs
DEMO_DIR			:= ${PACKAGE_DIR}/demos
PROTO_SRC_DIR		:= ../../docs/protobuf
PROTO_OUT_DIR		:= ${PACKAGE_DIR}/proto

PROTOC				:= protoc
PROTOCFLAGS			:= -I ${PROTO_SRC_DIR} --python_betterproto_out=${PROTO_OUT_DIR}
PROTOS				:= $(wildcard ${PROTO_SRC_DIR}/*.proto)
PROTO_OBJS			:= $(PROTOS:.proto=_pb.py)

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: clean format lint tests docs build ## Clean everything, then format code, lint, run tests, build docs, and build package

.PHONY: clean_tests
clean_tests: ## Clean raw coverage and html results
	@rm -rf htmlcov
	@rm -f .coverage

.PHONY: clean_generated
clean_generated: ## Clean all generated files
	@rm -f ${PROTO_OUT_DIR}/*pb*

.PHONY: generated
generated: protos ## Create all generated code

.PHONY: protos
protos: ${PROTO_OBJS} ## Generate all protobuf python files

%_pb.py: %.proto
	mv ${PROTO_OUT_DIR}/__init__.py ${PROTO_OUT_DIR}/temp
	${PROTOC} ${PROTOCFLAGS} $*.proto
	mv ${PROTO_OUT_DIR}/open_gopro.py ${PACKAGE_DIR}/proto/$(@F)
	mv ${PROTO_OUT_DIR}/temp ${PROTO_OUT_DIR}/__init__.py

.PHONY: tests
tests: clean_tests  ## Run PyTest and calculate test coverage
	@coverage run -m pytest

.PHONY: format
format: ## Run Black to format code
	echo "Running black to format all python code..."
	@black . --line-length 111 --exclude venv

.PHONY: lint
lint:  ## Run mypy for static typing analysis and flake8 for linting
	@echo "Performing static typing analysis..."
	@mypy open_gopro
	@echo "Linting..."
	@pylint open_gopro

.PHONY: clean_docs
clean_docs:  ## Remove generated docs
	@rm -f ${DOCS_DIR}/modules.rst
	@rm -rf ${DOCS_DIR}/build

.PHONY: docs-api-check
docs-api-check: lint ## Static analysis of docstrings for missing / errors
	@echo "Validating docstrings..."
	@pydocstyle -ve ${PACKAGE_DIR}

.PHONY: sphinx
sphinx: clean_docs ## Generate Sphinx documentation
	@echo "Building html documentation..."
	@cd ${DOCS_DIR} && sphinx-build -W -b html . build

.PHONY: docs
docs: clean_docs docs-api-check sphinx ## Generate all documentation with prerequisite checks.
	@echo Githubifying Sphinx output...
	@docs/sphinxtogithub

.PHONY: clean_build
clean_build: ## Clean build artifacts
	@rm -rf build dist

.PHONY: build
build: clean_build ## Build dist but do not publsih
	@python setup.py sdist

.PHONY: publish
publish: build  ## Build and publish to PyPi
	@twine upload dist/*

.PHONY: clean
clean: clean_tests clean_docs clean_build  ## Clean tests, docs, and build
