#! /bin/bash
while read imei imsi
do
if [[ ${imei:0:1} != "#" ]]; then
	trap "exit" SIGINT

	#change ip address	
	osascript ../ip_random.scpt

	echo $imei
	#restore imei for device
	python ../device_modify.py $imei $imsi
	python ninegame_emulate.py reactive

	sleep 2
	adb shell am force-stop cn.ninegame.gamemanager
	adb shell am start 'cn.ninegame.gamemanager/.activity.MainActivity'

	adb shell pm clear cn.ninegame.gamemanager
	sleep 2
fi
done < "9game_imei_list.2016-01-17"
