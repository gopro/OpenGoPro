# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:43 PM

# This must be run from the directory it exists in.

OPEN_GO_PRO_DIR		:=
PACKAGE_DIR			:= open_gopro
DOCS_DIR			:= docs
DEMO_DIR			:= ${PACKAGE_DIR}/demos
REPORTS_DIR			:= reports
PROTO_SRC_DIR		:= ../../docs/protobuf
PROTO_OUT_DIR		:= ${PACKAGE_DIR}/proto
COVERAGE_BADGE		:= ${DOCS_DIR}/_static/coverage.svg

PROTOC				:= protoc
PROTOCFLAGS			:= -I ${PROTO_SRC_DIR} --python_betterproto_out=${PROTO_OUT_DIR}
PROTOS				:= $(wildcard ${PROTO_SRC_DIR}/*.proto)
PROTO_OBJS			:= $(PROTOS:.proto=_pb.py)

######################################### General ############################################################

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: clean format lint tests docs build ## Clean everything, then format code, lint, run tests, build docs, and build package

.PHONY: clean_artifacts
clean_artifacts:
	@echo "Cleaning artifacts..."
	@$$(find . -type f -name '*.py[co]' -delete -o -type d -name '__pycache__' -delete)
	@$$(find . -type f -name '*.log' -delete)
	@$$(find . -type f -name '*.jpg' -delete)
	@$$(find . -type f -name '*.mp4' -delete)
	@$$(find . -type f -name '*.JPG' -delete)
	@$$(find . -type f -name '*.MP4' -delete)
	@$$(find . -type f -name '*.csv' -delete)
	@rm -rf .mypy_cache

.PHONY: clean
clean: clean_artifacts clean_tests clean_docs clean_build  ## Clean tests, docs, and build

.PHONY: reports
reports: ## Make the reports dir if it doesn't exist
	@mkdir -p ${REPORTS_DIR}

###################################### Generated Files #######################################################

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

########################################## Testing ###########################################################

.PHONY: clean_tests
clean_tests: ## Clean raw coverage and html results
	@echo "Cleaning tests..."
	@rm -rf ${REPORTS_DIR}
	@rm -rf .pytest_cache

.PHONY: unit_tests
unit_tests: # Run unit tests.
	@echo "Running unit tests..."
	@pytest tests/unit --cov-fail-under=70

.PHONY: e2e_tests
e2e_tests: # Run end to end tests (excluding demos).
	@echo "Running end-to-end tests..."
	@pytest -k 'not demos' tests/e2e

.PHONY: tests
tests: clean_tests ## Run all tests (unit, e2e, and demos) and calculate coverage.
	@echo "Running all tests..."
	@pytest tests

.PHONY: coverage
coverage: ## Build the coverage badge from the test results
	@echo "Building coverage badge..."
	@rm -f ${COVERAGE_BADGE}
	@coverage-badge -o ${COVERAGE_BADGE}

###################################### Static Code Analyis ###################################################

.PHONY: format
format: ## Run Black to format code
	@echo "Running black to format all python code..."
	@black . --line-length 111 --exclude venv

.PHONY: lint
lint: reports ## Run mypy for static typing analysis and pylint for linting
	@echo "Performing static typing analysis..."
	@mypy open_gopro | tee ${REPORTS_DIR}/linting
	@echo "Linting..."
	@pylint open_gopro | tee -a ${REPORTS_DIR}/linting

######################################### Documentation ######################################################

.PHONY: clean_docs
clean_docs:  ## Remove generated docs
	@echo "Cleaning docs..."
	@rm -f ${DOCS_DIR}/modules.rst
	@rm -rf ${DOCS_DIR}/build

.PHONY: docs-api-check
docs-api-check: clean_artifacts ## Static analysis of docstrings for missing / errors
	@echo "Validating docstrings..."
	@pydocstyle -ve ${PACKAGE_DIR}/** | tee ${REPORTS_DIR}/docstrings

.PHONY: sphinx
sphinx: clean_docs reports ## Generate Sphinx documentation
	@echo "Building html documentation..."
	@cd ${DOCS_DIR} && sphinx-build -W -b html . build
	@rm -rf ${DOCS_DIR}/build/.doctrees ${DOCS_DIR}/build/_sources ${DOCS_DIR}/build/_static/fonts

.PHONY: docs
docs: docs-api-check sphinx ## Generate all documentation with prerequisite checks.

############################################## Publishing ####################################################

.PHONY: clean_build
clean_build: ## Clean build artifacts
	@rm -rf build dist

.PHONY: build
build: clean_build ## Build dist but do not publish
	@python setup.py sdist

.PHONY: publish
publish: build  ## Build and publish to PyPi
	@twine upload dist/*
