#!/bin/bash



#rerun self in background - to simplyfy docker startup command
if [ "${1}"  != "bg" ] ; then
    "${BASH_SOURCE[0]}" bg "{args[@]}" 0<&- &
    sed -i -e "s/postgres:x:999:999/postgres:x:${TECH_USER_ID}:${TECH_GROUP_ID}/g"  /etc/passwd
    sed -i -e "s/postgres:x:999/postgres:x:${TECH_GROUP_ID}/g"  /etc/group
    /docker-entrypoint.sh postgres  ||  exit $?
fi

pg_hba_file=/var/lib/postgresql/data/pg_hba.conf
conf_file=/var/lib/postgresql/data/postgresql.conf

level=INFO
logMessage(){
    date=$(date "+%Y-%m-%d %T.%3N UTC")
    echo "$date" "${1}" "${2}"
}

#steps
# check if master or slave
# check postgers status

setupMaster(){
    sleep 3
    logMessage INFO "In master. Doing check for replication setup"
	i=30
	while [[ $i -gt 0 ]] ; do
	     logMessage INFO "Checking if postgres is up : ${i}s" 
	    cmd="gosu postgres pg_ctl status 2>&1 > /dev/null &&  gosu postgres psql -Atc \"select 1 from pg_roles where rolname='postgres'\";" 
        logMessage DEBUG "${cmd}"
	    out=$( eval "$cmd" )
	    [[ $out == "1" ]]  &&  break
        [[ $POSTGRES_CRASHED == 1 ]] && ( logMessage ERROR "Postgres start crashed... No point chekcing" ; exit 2 )
	    logMessage INFO "Unable to connect, waiting..."
	    i=$((  i - 1 ))
	    sleep 1
	done
    [[ $i -eq 0 ]] && ( logMessage ERROR "Timeout reached. Exiting.. " ; exit 1 )

    logMessage INFO "Check if replication user:${REPLICATION_USER} exists on master database"
    cmd="gosu postgres psql -Atc \"select 1 from pg_roles where '${REPLICATION_USER}'=rolname\";" 
    logMessage DEBUG "cmd: ${cmd}"
    out=$( eval "$cmd" )
    if  [[  $out  != "1" ]] ; then 
        logMessage INFO " No replicator user found, creating "
        cmd="gosu postgres psql -c \"CREATE USER ${REPLICATION_USER} REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '${REPLICATION_PASS}';\""
        logMessage DEBUG "cmd: ${cmd}"
        out=$( eval "${cmd}" )
    else
        echo "Replication user found. skipping"
    fi

    logMessage INFO "Checking entry in pg_hba"
    pg_hba_line="host\treplication\t${REPLICATION_USER}\tall\tmd5\n"
    reload_required=0
    if [[ $( grep "$( printf ${pg_hba_line})" ${pg_hba_file} | wc -l | xargs ) -eq 0 ]] ; then
        logMessage INFO "No replicator in pg_hba.conf, adding... "
        printf $pg_hba_line >> ${pg_hba_file}
        reload_required=1
    else
        logMessage INFO "Entry present in pg_hba"
    fi

    logMessage INFO "Checking entry in postgres.conf"
    postgres_line="wal_level = replica\nmax_wal_senders = 10\nwal_keep_segments = 64\n"
    if [[ $( grep -E "$( printf "${postgres_line_check}")" ${conf_file} | wc -l | xargs ) -eq 0 ]] ; then
        logMessage INFO "No requred conf in postgres.conf, adding..."
        grep -v  -e "wal_level" -e "max_wal_senders" -e "wall_keep_segments" -e "hot_standby" ${conf_file} > ${conf_file}.tmp
        mv ${conf_file}.tmp ${conf_file}
        printf "${postgres_line}" >> ${conf_file}
        reload_required=1
    else
        logMessage INFO "Entry present in postgres.conf"
    fi
    
    if [[ ${reload_required} -eq 1 ]] ; then
        logMessage INFO "Reload required"
        gosu postgres pg_ctl reload
    fi
    
}

setupSlave(){
    logMessage INFO "slave"
}


if [ "${IS_SLAVE}" == 'true' ] ; then
    setupSlave
else
    setupMaster
fi

