#!/bin/bash
sed -i -e "s/postgres:x:999:999/postgres:x:${TECH_USER_ID}:${TECH_GROUP_ID}/g"  /etc/passwd
sed -i -e "s/postgres:x:999/postgres:x:${TECH_GROUP_ID}/g"  /etc/group

pg_hba_file=/var/lib/postgresql/data/pg_hba.conf
conf_file=/var/lib/postgresql/data/postgresql.conf

level=INFO
logMessage(){
    date=$(date "+%Y-%m-%d %T.%3N UTC")
    echo "$date" "${1}" "${2}"
}

logMessage INFO "Creating .pgpass file with avaliable data"
gosu postgres echo "${MASTER_IP}:${MASTER_PORT}:replication:${REPLICATION_USER}:${REPLICATION_PASS}" > /var/lib/postgresql/.pgpass && chmod 600 /var/lib/postgresql/.pgpass && chown postgres var/lib/postgresql/.pgpass
gosu postgres echo "${MASTER_IP}:${MASTER_PORT}:postgres:${REPLICATION_USER}:${REPLICATION_PASS}" >> /var/lib/postgresql/.pgpass && chmod 600 /var/lib/postgresql/.pgpass && chown postgres var/lib/postgresql/.pgpass

logMessage INFO "Checking is user: ${REPLICATION_USER} can connet to: ${MASTER_IP}:${MASTER_PORT}"
cmd="gosu postgres psql -U ${REPLICATION_USER} -h ${MASTER_IP} -p ${MASTER_PORT} -d postgres -Atc \"select 1;\" 2>&1"
logMessage DEBIG "cmd: ${cmd}"
out=$( eval "$cmd" )
[[ ${out} != 1 ]] &&  logMessage ERROR "Master not avaliable... exiting" && exit 2 
#if [[ ${out} != 1 ]] ; then logMessage ERROR "Master not avaliable... exiting" ; exit 2 ;  fi

logMessage INFO "Master avaliable, creating base backup"
rm -rf /var/lib/postgresql/data/*
chown postgres:postgres /var/lib/postgresql/data
gosu postgres pg_basebackup -h ${MASTER_IP} -p ${MASTER_PORT} -D /var/lib/postgresql/data/ -U replicator --wal-method=fetch

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
postgres_line_check="^hot_stndby = on\n"
if [[ $( grep -E "$( printf "${postgres_line_check}")" ${conf_file} | wc -l | xargs ) -eq 0 ]] ; then 
    logMessage INFO "No requred conf in postgres.conf, adding..."
    grep -v  -e "wal_level" -e "max_wal_senders" -e "wall_keep_segments" -e "hot_standby" ${conf_file} > ${conf_file}.tmp
    mv ${conf_file}.tmp ${conf_file}
    postgres_line="wal_level = replica\nmax_wal_senders = 10\nwal_keep_segments = 64\nhot_standby = on\n"
    printf "${postgres_line}" >> ${conf_file}
fi

printf "standby_mode = 'on'\nprimary_conninfo = 'host=${MASTER_IP} port=${MASTER_PORT} user=${REPLICATION_USER} password=${REPLICATION_PASS}'\ntrigger_file = '/var/lib/postgresql/data//MasterNow'\n" >  /var/lib/postgresql/data/recovery.conf
chown postgres:postgres /var/lib/postgresql/data/recovery.conf


logMessage INFO "Starting postgres stand-by"
exec gosu postgres /docker-entrypoint.sh postgres
