# Makefile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:41 AM

mkfile_path = $(abspath $(lastword $(MAKEFILE_LIST))/..)

R_TOOLS_DIR := ${mkfile_path}
TUTORIALS_DIR := ${R_TOOLS_DIR}/../../tutorials

DOC_BUILDER	:= Rscript --vanilla ${R_TOOLS_DIR}/make_docs.R

RMDS	:= $(wildcard ${TUTORIALS_DIR}/*.Rmd ${TUTORIALS_DIR}/*/*.Rmd ${TUTORIALS_DIR}/*/*/*.Rmd ${TUTORIALS_DIR}/*/*/*/*.Rmd ${TUTORIALS_DIR}/*/*/*/*/*.Rmd)
HTMLS	:= $(RMDS:.Rmd=.html)

.PHONY: help
help: ## Display this help which is generated from Make goal comments
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1,$$2}'

.PHONY: install
install: ## Build and install htmlwidgets (currently just quiz)
	@cd ${R_TOOLS_DIR}/quiz && R -e 'devtools::document()'
	@cd ${R_TOOLS_DIR}/quiz && R -e 'devtools::install()'

.PHONY: tutorials
tutorials: ${HTMLS} ## Build rmarkdown files into HTML output

%.html: %.Rmd
	@echo Building $@ from $<
	@${DOC_BUILDER} -i $< -o $(@D)

.PHONY: clean_tutorials
clean_tutorials:  ## Remove built HTML output
	@rm -rf ${HTMLS}

.PHONY: clean  ## Clean everything (just html output for now)
clean: clean_tutorials