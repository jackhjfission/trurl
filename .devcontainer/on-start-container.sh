#!/usr/bin/env bash

echo "Running start up script."

chmod +x /home/klapaucius/workspace/.devcontainer/on-start-host.sh && \
    /home/klapaucius/workspace/.devcontainer/on-start-host.sh
