#!/bin/bash
#getting all opts
while getopts h:u:p:o: opt
do
   case $opt in
       h) hostnames=($OPTARG);;
       u) user=($OPTARG);;
       p) process=($OPTARG);;
       o) out=($OPTARG);;
   esac
done

while IFS='' read -r hostname
do
    scp isrunning.sh $user@$hostname:~/tmp/
    if [ssh $user@$hostname '(bash -s ~/tmp/isrunning.sh $process $user)' == 0]; then
	output=$(ssh $user@$hostname ls /tmp/ |grep $user |grep $process)
	echo "$output" > "$out"
        fi
done <<< "$hostnames"
