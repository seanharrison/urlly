#!/bin/bash
set -eu

# install git, direnv, docker, htpasswd
sudo apt-get update 
sudo apt-get install -y \
    git \
    direnv \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# docker debian repository
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
sudo apt-get update

# install docker
sudo apt-get install -y \
     docker-ce \
     docker-ce-cli \
     containerd.io

# install docker-compose
sudo curl -L \
    "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose

# hook direnv into the shell
echo 'eval "$(direnv hook bash)"' >>~/.bashrc

# check out urlly
git clone https://github.com/seanharrison/urlly
cd urlly

# create .envrc with all the necessary values
cp _envrc.TEMPLATE .envrc
echo "export POSTGRES_PASSWORD=$(openssl rand -hex 32)" >>.envrc

echo To finish the deployment:
echo 1. Edit .envrc with your HOST_NAME
echo 2. "source ~/.bashrc" to activate direnv, and "direnv allow" to load the environment.
echo 3. Initialize the docker stack with 'docker swarm init --advertise-addr [ipaddress]'
echo 4. Build the images with "docker-compose build"
echo 5. You can now 'docker stack deploy -c docker-compose.yml -c docker-compose-deploy.yml urlly'
