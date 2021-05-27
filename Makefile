# Makefile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:52 UTC 2021

ORIGINAL_VERSION=$(strip $$(awk '/Current Version: /{print $$NF}' README.md))
VERSION:=$(ORIGINAL_VERSION)

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean cached jekyll files
	@rm -rf docs/_site docs/.jekyll-cache docs/.jekyll-metadata docs/tutorials/_demos

.PHONY: prepare_demos
prepare_demos: ## Copy demos into docs folder for Jekyll building and add front matter
	@echo "Preparing demos..."
	@tools/prepare_demos

.PHONY: build
build: prepare_demos ## Build but do not serve the jekyll pages
	@docker-compose run --rm jekyll "bundle exec jekyll build --baseurl ${BASE_URL}"

.PHONY: serve
serve: prepare_demos ## Serve the sample site here
	@docker-compose up

.PHONY: version
version: ## Update the Open GoPro version
	@if test $(VERSION) == $(ORIGINAL_VERSION); then \
		echo "$(VERSION) is not a new version" ; false;\
	fi
	@echo "Updating version to $(VERSION)"
	@sed -i.bak "s/Current Version: $(ORIGINAL_VERSION)/Current Version: ${VERSION}/g" README.md && rm README.md.bak
	@make copyright

.PHONY: tests
tests: ## Run link checker. This assumes python installed and jekyll site is currently being served
	@pip install linkchecker
	@linkchecker http://127.0.0.1:5000/

.PHONY: copyright
copyright: ## Check for missing copyrights everywhere and add them using the version from README.md
	@echo "Verifying / adding copyrights..."
	@./tools/copyright -i . $(ORIGINAL_VERSION)

.PHONY: setup_docker
setup_docker: ## Build the docker image
	@docker-compose build jekyll

.PHONY: setup
setup: setup_docker ## Setup development environment