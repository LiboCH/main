#!/bin/bash
docker volume create -d local \
    -o device=/home/libo/git/liboch/main/playground/docker/07_postgres_docker/data-master \
    -o o=bind \
    -o type=none \
    vol.postgres-master

docker run -d --rm \
    -v vol.postgres-master:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=password \
    --name postgres-master-init \
    postgres:11.9

docker stop postgres-master-init

docker run -d --rm \
    -v vol.postgres-master:/var/lib/postgresql/data \
    bash chown -R 1000:1000 /var/lib/postgresql/data

#start and expose
docker run -it --rm \
    --user 1000:1000 \
    -e POSTGRES_PASSWORD=password \
    -v vol.postgres-master:/var/lib/postgresql/data \
    --name postgres-master \
    postgres:11.9

