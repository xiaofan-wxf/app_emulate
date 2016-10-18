device_ips=(192.168.1.92 192.168.1.72 192.168.1.98)

function device_connect(){
    for ip in ${device_ips[@]}
    do 	
        adb connect $ip
        adb -s $ip:5555 root 
    done
}

function device_disconnect(){
    for ip in ${device_ips[@]}
    do 
        adb disconnect $ip
    done
}
