# Makefile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb  4 21:36:17 UTC 2022


PROTO_SRC_DIR		:= ../../../protobuf
PROTO_OUT_DIR		:= ${PACKAGE_DIR}/proto
COVERAGE_BADGE		:= ${DOCS_DIR}/_static/coverage.svg

PROTOC				:= protoc
PROTOCFLAGS			:= -I ${PROTO_SRC_DIR} --python_betterproto_out=${PROTO_OUT_DIR}
PROTOS				:= $(wildcard ${PROTO_SRC_DIR}/*.proto)
PROTO_OBJS			:= $(PROTOS:.proto=_pb.py)
############### Generated Files #######################################################

.PHONY: clean_generated
clean_generated: ## Clean all generated files
	@rm -f ${PROTO_OUT_DIR}/*pb*

.PHONY: generated
generated: protos ## Create all generated code

.PHONY: protos
protos: ${PROTO_OBJS} ## Generate all protobuf python files

%_pb.py: %.proto
	@echo "building $(@F) from $(^F) ..."
	@mv ${PROTO_OUT_DIR}/__init__.py ${PROTO_OUT_DIR}/temp
	@${PROTOC} ${PROTOCFLAGS} $*.proto > /dev/null 2> /dev/null 2>&1
	@mv ${PROTO_OUT_DIR}/${PACKAGE_DIR}.py ${PROTO_OUT_DIR}/$(@F)
	@mv ${PROTO_OUT_DIR}/temp ${PROTO_OUT_DIR}/__init__.py

########################################## Testing ###########################################################

.PHONY: coverage
coverage: ## Build the coverage badge from the test results
	@echo "Building coverage badge..."
	@rm -f ${COVERAGE_BADGE}
	@coverage-badge -o ${COVERAGE_BADGE}


