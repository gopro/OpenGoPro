# Makefile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May 20, 2021  8:24:31 PM

all: make_all_demos

preview_stream: make_preview_stream_demo

ui_control: make_ui_control_demo

media_demo: make_media_demo

make_all_demos:
	mkdir -p bin
	mkdir -p inc
	mkdir -p src
	cd bin && cmake -G"Unix Makefiles" -DDEMO="all" -DREQUIRES_CJSON=1 ../
	cd bin && make

make_preview_stream_demo:
	mkdir -p bin
	mkdir -p inc
	mkdir -p src
	cd bin && cmake -G"Unix Makefiles" -DDEMO="stream_commands" ../
	cd bin && make

make_ui_control_demo:
	mkdir -p bin
	mkdir -p inc
	mkdir -p src
	cd bin && cmake -G"Unix Makefiles" -DDEMO="ui_control_commands" -DREQUIRES_CJSON=1 ../
	cd bin && make

make_media_demo:
	mkdir -p bin
	mkdir -p inc
	mkdir -p src
	cd bin && cmake -G"Unix Makefiles" -DDEMO="media_commands" -DREQUIRES_CJSON=1 ../
	cd bin && make