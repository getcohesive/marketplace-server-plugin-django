#!/usr/bin/env bash

# Clean up older build
rm -rf dist cohesive_marketplace_server_plugin_django.egg-info

# Run the build
python3 -m build

# Publish
python3 -m twine upload dist/*