#!/usr/bin/env bash

IMAGE_NAME="$(grep IMAGE_NAME .env | cut -d'=' -f2)"
IMAGE_VERSION="$(grep IMAGE_VERSION .env | cut -d'=' -f2)"

# build command for image
sudo docker build \
    -t $IMAGE_NAME:$IMAGE_VERSION \
    ../