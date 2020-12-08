#!/bin/bash
set -eu

# install git, direnv, docker, htpasswd
sudo apt-get update 
sudo apt-get install -y \
    # git
    git \
    # direnv for environment management
    direnv \
    # system prerequisites for docker
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
echo -n "SITE_NAME: "
read SITE_NAME
echo export SITE_NAME=$(SITE_NAME) >>.envrc
echo export 'SITE_HOST=http://${SITE_NAME}'
echo export POSTGRES_DB=urlly >>.envrc
echo export POSTGRES_USER=urlly >>.envrc
echo export POSTGRES_PASSWORD=$(openssl rand -hex 32) >>.envrc

echo You must initialize the docker stack with 'docker swarm init --advertise-addr [ipaddress]'
echo then you can 'docker stack deploy -c docker-compose.yml -c docker-compose-deploy.yml urlly'
