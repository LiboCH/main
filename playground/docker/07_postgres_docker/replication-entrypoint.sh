#!/bin/bash

#rerun self in background - to simplyfy docker startup command
if [ "${1}"  != "bg" ] ; then
    "${BASH_SOURCE[0]}" bg "{args[@]}" 0<&- &
    sed -i -e "s/postgres:x:999:999/postgres:x:${TECH_USER_ID}:${TECH_GROUP_ID}/g"  /etc/passwd
    sed -i -e "s/postgres:x:999/postgres:x:${TECH_GROUP_ID}/g"  /etc/group
    /docker-entrypoint.sh postgres
fi

level=INFO
logMessage(){
    date=$(date "+%Y-%m-%d %T.%3N UTC")
    echo "$date" "${1}" "${2}"
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
    logMessage INFO "slave"
else
    logMessage INFO "In master. Doing check for replication setup"
	i=30
	while [[ $i -gt 0 ]] ; do
	    echo "Checking if postgres is up : ${i}s" 
	    cmd="gosu postgres pg_ctl status 2>&1 > /dev/null &&  gosu postgres psql -Atc \"select 1 from pg_roles where rolname='postgres'\";" 
        logMessage DEBUG "${cmd}"
	    out=$( eval "$cmd" )
	    [[ $out == "1" ]]  &&  break
	    echo "Unable to connect, waiting..."
	    i=$((  i - 1 ))
	    sleep 1
	done

    [[ $i -eq 0 ]] && ( logMessage ERROR "Timeout reached. Exiting.. " ; exit 1 )


    logMessage "Check if replication user:$replication_user exists on master database"
    cmd="gosu postgres psql -tAc \"select 1 from pg_roles where '${replication_user}'=rolname\""
    logMessage "${cmd}"
    res=$(eval "${cmd}")
    logMessage "res:$res"
fi

