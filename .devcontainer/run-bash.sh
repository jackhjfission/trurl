#!/usr/bin/env bash

IMAGE_NAME="$(grep IMAGE_NAME .env | cut -d'=' -f2)"
IMAGE_VERSION="$(grep IMAGE_VERSION .env | cut -d'=' -f2)"

sudo docker run -it \
    --mount type=bind,src=$(dirname $(readlink -f $0))/../,dst=/home/jovyan/work \
    --user root \
    --env CONTAINER_NAME=${IMAGE_NAME}:${IMAGE_VERSION} \
    $IMAGE_NAME:$IMAGE_VERSION /bin/bash
