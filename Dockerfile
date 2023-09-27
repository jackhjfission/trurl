# reference: https://github.com/jupyter/docker-stacks/tree/main/images/scipy-notebook
FROM jupyter/scipy-notebook:2023-09-04

LABEL maintainer="jackhjfission <jackhjfission@gmail.com>"

USER root

# install quarto
RUN mkdir /home/jovyan/downloads && \
    wget -P /home/jovyan/downloads https://github.com/quarto-dev/quarto-cli/releases/download/v1.3.450/quarto-1.3.450-linux-amd64.deb && \
    dpkg -i /home/jovyan/downloads/quarto-1.3.450-linux-amd64.deb && \
    rm -fr /home/jovyan/downloads

COPY .devcontainer/on-start-image.sh /
RUN chmod +x /on-start-image.sh

USER ${NB_UID}

# install precommit and set up hooks
# this makes a throw-away git repo to encourage pre-commit
# to install hooks
RUN mkdir fake-repo
COPY .pre-commit-config.yaml fake-repo
RUN mamba install -y -c conda-forge pre-commit && \
    cd fake-repo && \
    git init && \
    pre-commit install --install-hooks && \
    cp .git/hooks/pre-commit /home/jovyan/.pre-commit && \
    cd .. && \
    rm -rf fake-repo && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" && \
    fix-permissions "/home/${NB_USER}/.cache/pre-commit"

CMD /on-start-image.sh ; start-notebook.sh