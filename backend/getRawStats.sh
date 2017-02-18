#!/bin/bash
# script to get more detailed xDSL stats from TP-Link web interface


# standard HTTP basic authentication, but set in cookie
. ../my_config.cfg
AUTH=$(echo -n "${user}:${password}" | base64)
IP="192.168.1.1"

POSTDATA=$'[STAT_CFG#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r
[STAT_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]1,0\r
'
main() {
	file=$1
	[ "$1" == "" ] && file="/dev/stdout"
	curl \
	   --data-binary "${POSTDATA}" \
	    --referer "http://${IP}/" \
	    --header "Cookie: Authorization=Basic ${AUTH}" \
	    --header "Content-Type: text/plain; charset=UTF-8" \
	    "http://${IP}/cgi?1&5" > $file 2>&1

}

main "$@"
exit 0
# Elaboration is now deprecated and done in python instead for performance reasons

dec2ip () {
    local ip dec=$@
    for e in {3..0}
    do
        ((octet = dec / (256 ** e) ))
        ((dec -= octet * 256 ** e))
        ip+=$delim$octet
        delim=.
    done
    echo $ip
}


declare -A TOTAL_BYTES
declare -A IP_ADDRESS
declare -A CURR_BYTES
index=0
interval=5
while read line
do
        initial="$(echo $line | head -c 1)"
        if [ "$initial" == $'[' ]; then
                index=$((index + 1))
        fi
        field=$( echo $line | awk -F"=" '{ print $1 }')
        value=$( echo $line | awk -F"=" '{ print $2 }')
        if [ "$field" == "totalBytes" ]; then
                TOTAL_BYTES[$index]=$value;
        fi
        if [ "$field" == "currBytes" ]; then
                CURR_BYTES[$index]=$value;
        fi
        if [ "$field" == "ipAddress" ]; then
                IP_ADDRESS[$index]=$(dec2ip $value)
        fi
	if [ "$field" == "interval" ]; then
		interval=$value
	fi
done < TMP_FILE

echo -n "["
for i in $(seq $index)
do
	if [ "${CURR_BYTES[$i]}" == "" ]; then
		curr_bytes=0
	else
		curr_bytes=${CURR_BYTES[$i]}
	fi 
	#printf "%s\t%s\t%s\n" ${IP_ADDRESS[$i]} ${TOTAL_BYTES[$i]} $(( (($curr_bytes * 8) / 1000) / 5 ))
	echo -n "{\"address\":\""${IP_ADDRESS[$i]}"\", \"current_bitrate\":\""$(( (($curr_bytes * 8) / 1000) / $interval ))"\"},"
done
echo "{}]"
