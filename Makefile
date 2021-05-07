# Makefile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 12:39:21 PM

MDS		:= README.md $(wildcard ./docs/*.md ./docs/*/*.md ./demos/swift/*/*.md)
HTMLS	:= $(MDS:.md=.html)

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: tutorials html ## Build everything (tutorials and html documentation)

.PHONY: clean
clean: clean_tutorials clean_html ## Clean everything (tutorials and html documentation)

.PHONY: copyright
copyright: ## Check for missing copyrights everywhere and add them using the version from README.md
	@echo "Verifying / adding copyrights..."
	@awk '/Current Version: /{print $$NF}' README.md | xargs ./tools/hooks/copyright -i .

.PHONY: clean_tutorials
clean_tutorials: ## Delete generated .html tutorial files
	@echo "Deleting generated .html tutorials"
	@docker-compose run --rm docs bash -c "make -f tools/rdocs/Makefile clean_tutorials"

.PHONY: tutorials
tutorials: ## Build tutorials using docker container
	@docker-compose run --rm docs

.PHONY: setup_docker
setup_docker: ## Build the docker image
	@docker-compose build docs

.PHONY: html
html: ${HTMLS} ## Build html from md files using docker container

# Use pandoc to build simple html from md and change any md links to html
%.html: %.md
	@echo Building $@ from $<
	@docker-compose run --rm docs bash -c "cat $< | sed 's/.md)/.html)/g' | pandoc -o $@ "

.PHONY: html
clean_html: ## Delete generated html files
	@echo "Removing generated html files"
	@rm -f ${HTMLS}

.PHONY: setup_hooks
setup_hooks: ## Install Git hooks
	@echo "Installing git hooks..."
	@cp tools/hooks/pre-commit .git/hooks

.PHONY: setup
setup: setup_hooks setup_docker ## Setup development environment