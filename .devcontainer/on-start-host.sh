#!/usr/bin/env bash

echo copying git pre-commit hook script
cp /home/jovyan/.pre-commit /home/jovyan/work/.git/hooks/pre-commit

# install the local package
pip install --no-deps --no-build-isolation -e /home/jovyan/work
# pin dependencies for local package and install them
chmod +x /home/jovyan/work/.devcontainer/pin-deps
mamba install -y $(/home/jovyan/work/.devcontainer/pin-deps)