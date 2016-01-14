#!/bin/bash
while [ -z "$(sh -c "adb devices" | sed -n 2p)" ]; do
	echo "no device-----wait----"
	sleep 3
done
echo "device $(sh -c "adb devices" | sed -n 2p | awk '{print $1}') connected----"
