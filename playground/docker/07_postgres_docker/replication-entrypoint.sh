#!/bin/bash

#rerun self in background - to simplyfy docker startup command
if [ "${1}"  != "bg" ] ; then
    "${BASH_SOURCE[0]}" bg "{args[@]}" 0<&- &
    exit 0 
fi

level=INFO
logMessage(){
    date=$(date "+%Y-%m-%d %T.%3N UTC")
    echo "$date" "$level" "${1}"
}

#steps
# check if master or slave
# check postgers status

master_ip=192.168.0.116
master_port=5432
slave_ip=192.168.0.116
slave_port=5431
replication_user=postgres
replication_password=replica

if [ "${IS_SLAVE}" == 'true' ] ; then
    logMessage "slave"
else
    logMessage "master"
    sleep 2
    logMessage "Check if replication user:$replication_user exists on master database"
    cmd="gosu postgres psql -tAc \"select 1 from pg_roles where '${replication_user}'=rolname\""
    logMessage "${cmd}"
    res=$(eval "${cmd}")
    logMessage "res:$res"
fi

