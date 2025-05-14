#!/bin/bash

set -e
trap 'echo "error on line $LINENO"; exit 1' ERR

host=$1
ping -c1 $host > /dev/null 2> /dev/null
[[ $? == 0 ]] && echo "$host is up" || echo "$host is down/not reachable"
