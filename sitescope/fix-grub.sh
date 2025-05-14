#!/bin/sh

mv $(readlink -f /boot/grub2/grubenv) /tmp
grub2-editenv /boot/grub2/grubenv create
grep -v ^# /tmp/grubenv > /tmp/a.sh
sed -i 's/^/"/' /tmp/a.sh
sed -i 's/$/"/' /tmp/a.sh
sed -i 's!^!grub2-editenv /boot/grub2/grubenv set !' /tmp/a.sh
