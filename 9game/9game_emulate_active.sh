#! /bin/bash

while true; do
	trap "exit" SIGINT
	#change ip address	
	osascript ../ip_random.scpt

	#modify imei and save to file
	python ../device_modify.py random

	sleep 1
	imei=$(cat device_imei.txt)

	#regis an account for superr fleet
	python ninegame_emulate.py active $imei

	#clean super fleet cache info
	adb shell am force-stop cn.ninegame.gamemanager
	adb shell am start 'cn.ninegame.gamemanager/.activity.MainActivity'
	sleep 8

	adb shell pm clear cn.ninegame.gamemanager

	sleep 2
done
