#!/bin/bash


today=$(date +"%Y%m%d")
tomorrow=$(date --date="tomorrow" +"%Y%m%d")

for h in `cat 0000.txt`
do
./manage_sitescope_mon_2.py -a disable -t ${today}2355 --hostname $h
done

echo "============================="
for h in `cat 0200.txt`
do
./manage_sitescope_mon_2.py -a disable -t "${tomorrow}0155" --hostname $h
done

echo "============================="

for h in `cat 0400.txt`
do
./manage_sitescope_mon_2.py -a disable -t "${tomorrow}0355" --hostname $h
done

echo "============================="

for h in `cat 0600.txt`
do
./manage_sitescope_mon_2.py -a disable -t "${tomorrow}0555" --hostname $h
done
echo "============================="

