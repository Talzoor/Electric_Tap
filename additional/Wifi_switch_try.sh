#!/bin/bash

LOGFILE=/home/pi/wifi_try.log
# Define a timestamp function
timestamp() {
date +"%Y/%m/%d %T"
}
var_ip() {
hostname -I
}

echo "test Started -- $(timestamp) -- IP:$(var_ip) " >> $LOGFILE

if [ 't' == 't' ]; then
	sleep 2
	ifconfig wlan0 down >> $LOGFILE 
	sleep 2
	ifconfig wlan0 up  >> $LOGFILE 
	sleep 2
	ifconfig wlan0 10.100.102.105  >> $LOGFILE 
fi

echo "End -- $(timestamp) -- IP:$(var_ip) " >> $LOGFILE
