.PHONY: all clean

SHELL := /bin/bash
RENPY := ../renpy-8.3.3-sdk
FOLDER := $(shell pwd)

all: move_images build move_images_back

# Create a temporary directory and move session images
move_images:
	@mkdir -p tmp && dir_tmp=$$(mktemp -d "tmp/dirmakeXXXX") && \
	mkdir -p $${dir_tmp} && \
	mv game/images/session* $${dir_tmp} 2>/dev/null || true

# Build and distribute the project using Ren'py
build:
	cd $(RENPY) && \
	./renpy.sh launcher distribute $(FOLDER)

# Move the session images back to the original folder
move_images_back:
	@mv tmp/dirmake*/* game/images/ 2>/dev/null || true
	@rm -d tmp/dirmake* 2>/dev/null || true

# Clean up temporary directories if needed
clean:
	rm -rf tmp/dir*
