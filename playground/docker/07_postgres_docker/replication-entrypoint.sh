#!/bin/bash

#rerun self in background - to simplyfy docker startup command
if [ "${1}"  != "bg" ] ; then
    "${BASH_SOURCE[0]}" bg "${args[@]}" 0<&- &
    exit 0 
fi

level=INFO
logMessage(){
    date=`date "+%Y-%m-%d %T.%3N UTC"`
    echo $date $level ${1}
}

#steps
# check if master or slave
# check postgers status


while :; do
    logMessage "test"
    sleep 1
done
