# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jan  5 23:22:12 UTC 2022

# This must be run from the directory it exists in.

SHELL				:= bash

PACKAGE_DIR			:= tutorial_modules
REPORTS_DIR			:= reports

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
	@$$(find . -type f -name '*.gpmf' -delete)
	@rm -rf .mypy_cache

.PHONY: clean
clean: clean_artifacts clean_tests  ## Clean tests, docs, and build

.PHONY: reports
reports: ## Make the reports dir if it doesn't exist
	@mkdir -p ${REPORTS_DIR}

########################################## Testing ###########################################################

.PHONY: clean_tests
clean_tests: ## Clean raw coverage and html results
	@echo "Cleaning tests..."
	@rm -rf ${REPORTS_DIR}
	@rm -rf .pytest_cache
	@rm -f .coverage

.PHONY: tests
tests: clean_tests ## Run all tests (unit, e2e, and demos) and calculate coverage.
	@echo "Running all tests..."
	@pytest tests

###################################### Static Code Analyis ###################################################

.PHONY: format
format: ## Run Black to format code
	@echo "Running black to format all python code..."
	@black --line-length 111 tutorial_modules tests setup.py

.PHONY: lint
lint: reports ## Run mypy for static typing analysis and pylint for linting
	@echo "Performing static typing analysis..."
	@set -o pipefail; mypy ${PACKAGE_DIR} | tee ${REPORTS_DIR}/linting
	@echo "Linting..."
	@set -o pipefail; pylint ${PACKAGE_DIR} | tee -a ${REPORTS_DIR}/linting
