#!/bin/bash

mods="cramfs squashfs udf"
r1=""
for m in $mods
do
    lsmod | grep $m
    if [ $? -eq 1 ]
    then
        res="no"
    else
        res="yes"
    fi
    r1="${r1}$res,"
done
r1=$(echo $r1 | sed -e 's/\,$//')
printf "%s,%s" $(hostname) $r1

