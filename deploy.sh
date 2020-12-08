#!/bin/bash
set -eu

git pull
export TAGNAME=$(git rev-parse --short HEAD)

docker-compose build
docker tag urlly_router urlly_router:$TAGNAME
docker tag urlly_app urlly_app:$TAGNAME

docker stack deploy -c docker-compose.yml -c docker-compose-deploy.yml $STACK_NAME --prune
