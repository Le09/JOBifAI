.PHONY: all clean

SHELL := /bin/bash
RENPY := ../renpy-8.3.0-sdk
FOLDER := $(shell pwd)

all: config_prepare move_images build move_images_back config_undo

no_demo: move_images build move_images_back

# Load environment variables from .keys.rc
config_prepare:
	@source ".keys.rc" && \
	sed -i "s/PRODIA_DEMO_KEY/$${prodia_api_key}/" game/config.rpy && \
	sed -i "s/LLM_DEMO_KEY/$${groq_api_key}/" game/config.rpy

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

# Undo the changes made to the configuration file
config_undo:
	@source ".keys.rc" && \
	sed -i "s/$${prodia_api_key}/PRODIA_DEMO_KEY/" game/config.rpy && \
	sed -i "s/$${groq_api_key}/LLM_DEMO_KEY/" game/config.rpy

# Clean up temporary directories if needed
clean:
	rm -rf tmp/dir*
