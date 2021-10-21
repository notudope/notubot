#!/bin/bash

RUNDIR=${PWD}
BOTDIR=$(dirname $(realpath ${0}))
UNIXTIME=$(date +%s)

if [ -z ${1} ] || [ ${1} == "-x" ] ; then
	cd ${BOTDIR}
	python3 -m notubot
	RETVAL=${?}
	cd ${RUNDIR}
	exit $RETVAL
elif [ ${1} == "-d" ] || [ ${1} == "--daemonize" ] ; then
	echo -e "I: Running silently in the background like a ninja..."
	cd ${BOTDIR}
	
	nohup python3 -m notubot >>${UNIXTIME}-notubot.log 2>&1 & echo "I: NOTUBOT PID is ${!}"
	deactivate
	cd ${RUNDIR}
	exit 0
elif [ ${1} == "-h" ] || [ ${1} == "--help" ] ; then
	echo -e "notubot"
	echo -e  "Licensed under Raphielscape Public License"
	echo -e "\nUsage:"
	echo -e "[no arguments] || -x -- Run in the foreground, stdout is the logcat"
	echo -e "--daemonize    || -d -- Run in the background, logs will be saved in *-notubot.log"
	exit 0
else
	echo -e  "notubot"
        echo -e  "Licensed under GNU General Public License v3.0"
        echo -e  "\nUsage:"
        echo -e  "[no arguments] || -x -- Run in the foreground, stdout is the logcat"
        echo -e  "--daemonize    || -d -- Run in the background, logs will be saved in *-notubot.log"
	exit 127
fi
