# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:25 PM

ORIGINAL_VERSION=$(strip $$(awk '/Current Version: /{print $$NF}' README.md))
VERSION:=$(ORIGINAL_VERSION)
# Default to public deployment. Anything else must be set at Make time
HOST_URL:=https://gopro.github.io
BASE_URL:=/OpenGoPro

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean cached jekyll files
	@echo "🧼 Cleaning jekyll artifacts..."
	-@docker-compose down > /dev/null 2>&1
	@rm -rf docs/_site docs/.jekyll-cache docs/.jekyll-metadata docs/tutorials/_demos docs/_conf-temp.yml

.PHONY: protos
protos: ## Generate markdown documentation from protobuf files
	@echo "📇 Building protobuf documentation..."
	@MSYS_NO_PATHCONV=1 docker run --rm \
		-v $$(pwd)/docs:/out \
		-v $$(pwd)/protobuf:/protos \
		pseudomuto/protoc-gen-doc --doc_opt=/out/_layouts/protobuf_markdown.tmpl,protos.md

.PHONY: config
config: # Create the jekyll config file specific to the site we are building
	@echo "🛠️ Configuring Jekyll site ${HOST_URL}${BASE_URL}"
	@echo "url: ${HOST_URL}" > ./docs/_config-temp.yml
	@echo "baseurl: ${BASE_URL}" >> ./docs/_config-temp.yml

.PHONY: prepare_jekyll
prepare_jekyll: setup clean demos protos config

.PHONY: build
build: prepare_jekyll ## Build but do not serve the jekyll pages
	@echo "🏗️ Building jekyll site..."
	@docker-compose run --rm --service-ports --detach --name plant_uml plant_uml
	@docker-compose run --rm jekyll bundle exec jekyll build --config _config.yml,_config-temp.yml
	@docker kill plant_uml > /dev/null 2>&1

.PHONY: serve
serve: HOST_URL=http://localhost:4998/
serve: BASE_URL=\"\"
serve: prepare_jekyll ## Serve the site locally at http://localhost:4998/
	@echo "🚦 Serving jekyll site..."
	-@docker-compose up --force-recreate

.PHONY: tests
tests: HOST_URL=http://jekyll:4998/
tests: BASE_URL=\"\"
tests: prepare_jekyll ## Clean everything, build, then run link checker.
	@./tools/check_links

.PHONY: version
version: ## Update the Open GoPro version
	@if test $(VERSION) == $(ORIGINAL_VERSION); then \
		echo "$(VERSION) is not a new version" ; false;\
	fi
	@echo "⬆️ Updating version to $(VERSION)"
	@sed -i.bak "s/Current Version: $(ORIGINAL_VERSION)/Current Version: ${VERSION}/g" README.md && rm README.md.bak
	@make copyright

.PHONY: copyright
copyright: ## Check for and add missing copyrights
	@echo "©️ Verifying / adding copyrights..."
	@./tools/copyright -i . $(ORIGINAL_VERSION)

.PHONY: setup_docker
setup_docker:
	@echo "🐳 Setting up docker images..."
	@docker-compose pull

.PHONY: setup
setup: setup_docker ## Setup development environment
