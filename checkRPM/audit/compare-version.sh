#!/bin/bash


#pattern="^([0-9a-zA-Z\-\.\+]+)-(\d\.)+\d+\-\d\..*"
pattern="^(.+)\.[^\.\-]+$"
pattern2="^([^\.]+)\-([0-9]+)\.([0-9]+)(\.[0-9]+)?(.[0-9]+)?(.[a-z0-9]+)?(\-[0-9]+).*$"

for p in `cat /tmp/EY-shouldbe/EY-shouldbe.txt`
do
if [[ "$p" =~ $pattern ]]
then
name_ver_rel=${BASH_REMATCH[1]}
#echo $name_ver_rel
if [[ "$name_ver_rel" =~ $pattern2 ]]
then
        echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]} ${BASH_REMATCH[3]} ${BASH_REMATCH[4]} ${BASH_REMATCH[5]} ${BASH_REMATCH[6]} ${BASH_REMATCH[7]}"
else
        echo "not match"
fi
fi
done

#rpm -qa --qf '%{NAME}-%{version}\n'