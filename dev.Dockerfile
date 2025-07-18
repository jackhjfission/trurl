FROM python:3.12-slim
LABEL maintainer="jackhjfission <jackhjfission@gmail.com>"

ARG USER_NAME=devuser

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash ${USER_NAME} && mkdir -p /home/${USER_NAME}/workspace && chown ${USER_NAME} /home/${USER_NAME}/workspace

# Switch to non-root user
USER ${USER_NAME}

# Install pipx via official installer for the user
RUN python -m pip install --user pipx
ENV PATH="/home/${USER_NAME}/.local/bin:$PATH"

# Ensure pipx is in PATH
RUN python -m pipx ensurepath

# Install Poetry and pre-commit
RUN pipx install poetry
RUN pipx install pre-commit

# install precommit and set up hooks
# this makes a throw-away git repo to encourage pre-commit
# to install hooks
RUN cd /home/${USER_NAME} && mkdir fake-repo
COPY /.pre-commit-config.yaml /home/${USER_NAME}/fake-repo
RUN cd /home/${USER_NAME}/fake-repo && \
    git init && \
    pre-commit install --install-hooks && \
    cp .git/hooks/pre-commit /home/${USER_NAME}/.pre-commit && \
    cd .. && \
    rm -rf /home/${USER_NAME}/fake-repo

COPY --chown=${USER_NAME}:${USER_NAME} /.devcontainer/on-start-container.sh /home/${USER_NAME}/
RUN chmod +x /home/${USER_NAME}/on-start-container.sh

USER ${USER_NAME}
