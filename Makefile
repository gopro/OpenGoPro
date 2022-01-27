# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:25 PM

ORIGINAL_VERSION=$(strip $$(awk '/Current Version: /{print $$NF}' README.md))
VERSION:=$(ORIGINAL_VERSION)
BASE_URL:=''
JEKYLL_CONFIG:=local

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean cached jekyll files
	@echo "🧼 Cleaning jekyll artifacts..."
	-@docker-compose down > /dev/null 2>&1
	@rm -rf docs/_site docs/.jekyll-cache docs/.jekyll-metadata docs/tutorials/_demos

.PHONY: prepare_demos
prepare_demos: ## Copy demos into docs folder for Jekyll building and add front matter
	@echo "📚 Preparing demos..."
	@tools/prepare_demos

.PHONY: build
build: clean prepare_demos ## Build but do not serve the jekyll pages
	@echo "🏗️ Building jekyll site..."
	@JEKYLL_CONFIG=${JEKYLL_CONFIG} docker-compose run --rm jekyll bundle exec jekyll build --baseurl ${BASE_URL} --config _config.yml,_config-${JEKYLL_CONFIG}.yml

.PHONY: serve
serve: clean prepare_demos ## Serve the site locally at http://127.0.0.1:4998/
	@echo "🚦 Serving the ${JEKYLL_CONFIG} site"
	-@JEKYLL_CONFIG=${JEKYLL_CONFIG} docker-compose run --rm --service-ports jekyll

.PHONY: tests
tests: JEKYLL_CONFIG=test
tests: build ## Clean everything, build, then serve in order to check all links.
	@echo; echo "🚦 Serving the test site"
	@JEKYLL_CONFIG=${JEKYLL_CONFIG} docker-compose run --rm --service-ports --detach jekyll
	@echo; echo "⏳ Waiting for server to be ready..."
	@until curl http://127.0.0.1:4998 > /dev/null 2>&1; do \
		:; \
	done
	@echo; echo "🔗 Checking links"
	-@JEKYLL_CONFIG=${JEKYLL_CONFIG} docker-compose run -T --rm --service-ports linkchecker | tee link_results
	@echo; echo "🧺 Parsing link checker results to remove server side problems..."; echo
	@tools/parse_linkchecker_results link_results
	@rm link_results

.PHONY: version
version: ## Update the Open GoPro version
	@if test $(VERSION) == $(ORIGINAL_VERSION); then \
		echo "$(VERSION) is not a new version" ; false;\
	fi
	@echo "⬆️ Updating version to $(VERSION)"
	@sed -i.bak "s/Current Version: $(ORIGINAL_VERSION)/Current Version: ${VERSION}/g" README.md && rm README.md.bak
	@make copyright

.PHONY: copyright
copyright: ## Check for missing copyrights everywhere and add them using the version from README.md
	@echo "©️ Verifying / adding copyrights..."
	@./tools/copyright -i . $(ORIGINAL_VERSION)

.PHONY: setup_docker
setup_docker: ## Build the docker image
	@echo "🐳 Setting up docker images..."
	@JEKYLL_CONFIG=local docker-compose pull --quiet

.PHONY: setup
setup: setup_docker ## Setup development environment

.PHONY: publish
publish: ## Publish the docker image (for internal use only)
	@docker-compose build
	@docker-compose push