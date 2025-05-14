#!/bin/bash

uname -a > /var/tmp/osinfo.txt
yum update -y > /var/tmp/os-update.txt 2>&1
reboot
