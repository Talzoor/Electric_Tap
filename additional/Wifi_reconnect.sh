#!/bin/bash

# Define a timestamp function
timestamp() {
date +"%Y/%m/%d %T"
}
curr_ip() {
#ifconfig wlan0 | grep 'inet' | cut -d: -f2 | awk '{print $2}'
hostname -I | awk '{print $1}'
}
static_ip() {
cat /etc/dhcpcd.conf | grep "interface wlan0" -A4 | grep "static ip_address" | sed -e 's/^.*\(=.*\/\).*$/\1/' -e 's/[static ip_address=/]//g'
}

printf "Started \t-- $(timestamp) -- IP:$(curr_ip)"

WEB=www.google.com
PACKETS=4
LOGFILE=/home/pi/wifi_check.log

count=$(ping -c $PACKETS -W 2 -n -B -s 0 -i 1 -l 1 -q $WEB | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')

re='^[0-9]+$'
if ! [[ $count =~ $re ]] ; then
	count=0
fi

if [ $count == 0 ]; then
	printf " -> failed. reconnect\n"
	sudo ifconfig wlan0 down 
        sleep 2
        sudo ifconfig wlan0 up
	sleep 5
else
	printf " -> passed.($count)\n"
	printf "\t\tIP check: now=$(curr_ip), static=$(static_ip)"

	if [ $(curr_ip) == $(static_ip)  ]; then
		printf " -> OK\n"
	else
		printf " -> Not good - changing\n"
		sudo ifconfig wlan0 $(static_ip)
		sleep 2
		sudo ip route add default via 10.100.102.1 #adding default routing for DNS
	fi
fi
