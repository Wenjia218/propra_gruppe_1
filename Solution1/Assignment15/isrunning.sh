#!/bin/bash

# is supposed to print 0 if process is not active anymore and print 1 if process is active

searched_process=$1
user=$2

processes=$(ps -u $user)

if echo $processes|grep $searched_process
then
	exit 1
else
	exit 0
fi





