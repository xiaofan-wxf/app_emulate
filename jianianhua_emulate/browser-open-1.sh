#! /bin/bash
num=1
while true; do
    trap "exit" SIGINT
    adb root -s $1 &>/dev/null
    adb -s $1 shell svc vpn on aaaa 59.s77.cn by863 333
    echo 'waiting for vpn reconnect.....'
    sleep 8

    max=`expr $RANDOM % 5`
    max=$(($max + 5))
    for i in $(seq $max)
    do  
        adb -s $1 shell pm clear com.android.browser &>/dev/null

        num=$(( $num + 1 ))    
        echo 'open browser with url' $num'.....'                              
        python browser-open-url.py $1    
    done
done
