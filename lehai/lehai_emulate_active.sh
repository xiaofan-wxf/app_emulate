#! /bin/bash

for i in `seq 250` 
do
	trap "exit" SIGINT
	#change ip address	
	osascript ../ip_random.scpt

	#modify imei and save to file
	python ../device_modify.py random

	sleep 1
	#imei=$(cat device_imei.txt)
	read imei imsi < device_imei.txt

	echo imei=$imei imsi=$imsi

	#regis an account for superr fleet
	python lehai_emulate.py active $imei $imsi

	#clean super fleet cache info
	adb shell am force-stop com.lehai.ui
	adb shell am start 'com.lehai.ui/com.showself.ui.LoadingActivity'
	sleep 8

	adb shell pm clear com.lehai.ui
	sleep $(($RANDOM%6))
done
