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
    scp isrunning.sh zhongw@$hostname:~/tmp/
    if [ $(ssh zhongw@$hostname '(bash -s ~/tmp/isrunning.sh $process $user)') ]; then
	echo "$hostname"
        fi
done < "$hostnames"

#der obenstehende Code ist unser Ansatz für die Lösung, hat aber leider nicht funktioniert
#wir sind manuell durch alle remote Kennungen und haben mit dem Skript is_running.sh den richtigen gefunden
# jedoch hatten wir zwei Ergebnisse: "rhodonit" und "sodalith" 
# leider haben den Plotten nicht geschafft wegen der Zeit