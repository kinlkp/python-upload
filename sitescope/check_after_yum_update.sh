#!/bin/bash

if [ $# -gt 0 ]
then
    expected_kernel=$1
    current_kernel=$(uname -r | sed -e 's/\.el[0-9].*//')
    if [ "$expected_kernel" != "$current_kernel" ]
    then
        dnf remove "kernel-core-$expected_kernel.el8" -y
        dnf install "kernel-core-$expected_kernel.el8" -y
        reboot
    else
        uname -a > /var/tmp/osinfo-after-yum.txt
        echo "Completed: kernel version is up-to-date. ($current_kernel)"
        exit 0
    fi
else
    echo "Error: script parameter 'kernel version' is not added."
    exit 1
fi
