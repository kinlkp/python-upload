#!/bin/bash


repo_gpgkey() {
    if grep -r "gpgkey" /etc/yum.repos.d/* /etc/dnf/dnf.conf
    then
        echo 1
    else
        echo 0
    fi
}

check_mod() {
    if grep -E "^install\s+$1\s+/bin/false" /etc/modprobe.d/* > /dev/null && \
        grep -E "^blacklist\s+$1" /etc/modprobe.d/* > /dev/null
    then
        echo 1
    else
        echo 0
    fi
}

mountoptions() {
    if findmnt -nk $1 | grep nodev | grep noexec | grep nosuid > /dev/null
    then
        echo 1
    else
        echo 0
    fi
}

main() {
    check_mod "cramfs"
    check_mod "freevxfs"
    check_mod "hfs"
    check_mod "hfsplus"
    check_mod "jffs2"
    check_mod "squashfs"
    check_mod "udf"
    check_mod "usb-storage"
    mountoptions "/tmp"
    mountoptions "/dev/shm"
    mountoptions "/var/"
    mountoptions "/var/log"
    mountoptions "/var/log/audit"
    mountoptions "/var/tmp"
}

main