#!/usr/bin/env bash

echo copying git pre-commit hook script
cp /home/klapaucius/.pre-commit /home/klapaucius/workspace/.git/hooks/pre-commit

# keep poetry env up to date
cd /home/klapaucius/workspace && poetry install --all-extras --all-groups

# start poetry environment when starting a terminal
echo "cd /home/${USER_NAME}/workspace && eval $(poetry env activate)" >> /home/${USER_NAME}/.bashrc

sleep 5
