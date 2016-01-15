#! /bin/bash

while true; do
	trap "exit" SIGINT
	#change ip address	
	osascript ../ip_random.scpt

	#modify imei and save to file
	python ../device_modify.py random

	sleep 1
	read imei imsi < device_imei.txt

	#regis an account for superr fleet
	python 360mobile_emulate.py active $imei $imsi

	sleep $(($RANDOM%6))
	#clean super fleet cache info
	adb shell am force-stop com.qihoo360.mobilesafe
	adb shell am start 'com.qihoo360.mobilesafe/.ui.index.AppEnterActivity'
	sleep $(($RANDOM%6))

	adb shell am force-stop com.qihoo360.mobilesafe
	adb shell am start 'com.qihoo360.mobilesafe/.ui.index.AppEnterActivity'
	sleep 8

	adb shell pm clear com.qihoo360.mobilesafe

	sleep $(($RANDOM%6))
done
