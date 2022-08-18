FROM gitpod/workspace-python-3.10

USER gitpod

# Install libhdf5
RUN sudo install-packages libhdf5-dev

# Install MongoDB
RUN \
    wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list \
    && sudo apt-get update \
    && sudo install-packages -y mongodb-org

RUN sudo mkdir -p /data/db && sudo chown -R gitpod /data/db

# Install Poetry
RUN pip install poetry
