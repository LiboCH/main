#!/bin/bash
#TODO: check if volume exist if not, create it
docker volume create -d local \
    -o device=/home/libo/git/liboch/main/playground/docker/07_postgres_docker/data-master \
    -o o=bind \
    -o type=none \
    vol.postgres-master

#TODO: check if there are some running leftovers
docker run -d --rm \
    -v vol.postgres-master:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=password \
    --name postgres-master-init \
    postgres:11.9

i=30
while [[ $i -gt 0 ]] ; do
    echo "Checking if postgres is up : ${i}s" 
    cmd="docker exec -it postgres-master-init gosu postgres psql -Atc \"select 1 from pg_roles where 'postgres'=rolname\";"
    out=$( eval "$cmd" )
    [[ ${out} ]]  && break
    i=$((  i - 1 ))
    sleep 1
done
#TODO: if timeout reached 

replication_user=replicator
replication_pass=replicator


cmd="docker exec -it postgres-master-init gosu postgres psql -Atc \"select 1 from pg_roles where '$replication_user'=rolname\";"
out=$( eval "$cmd" )
echo "out is: $out"
if  [[ $out -ne 1 ]] ; then 
    echo " No replicator user found, creating "
    cmd="docker exec -it postgres-master-init gosu postgres psql -Atc \"CREATE USER $replication_user REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '$replication_pass';\""
    echo "${cmd}"
    echo 
    out=$(( eval "${cmd}"))
else
    echo "Replication user found. skipping"
fi
exit
docker stop postgres-master-init

#TODO: add missing user to /etc/passwd ?? 
docker run -d --rm \
    -v vol.postgres-master:/var/lib/postgresql/data \
    bash chown -R 1000:1000 /var/lib/postgresql/data

#start and expose 
docker run -it --rm \
    --user 1000:1000 \
    -e POSTGRES_PASSWORD=password \
    -v vol.postgres-master:/var/lib/postgresql/data \
    -p 5432:5432  \
    --name postgres-master \
    postgres:11.9

