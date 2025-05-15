#!/usr/bin/bash

remote_name=$1

# choose fourth column of loadavg, because it shows the capacity of remote
# and how many processes are currently running


ssh folwark@$remote_name.cip.ifi.lmu.de "cat /proc/loadavg | cut -d ' ' -f 4"


# shows loadavg and takes fourth column
#print on output

