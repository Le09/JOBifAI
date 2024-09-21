#!/bin/bash

# Copy the pre-commit hook into the .git/hooks directory
cp hooks/pre-commit .git/hooks/pre-commit

# Make it executable
chmod +x .git/hooks/pre-commit

echo "Git hook installed successfully!"

