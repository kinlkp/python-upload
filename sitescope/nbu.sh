#!/bin/bash

set -e
trap 'echo "Error on line $LINENO"; exit 1' ERR

api_key=$n2_nbu_api
clientname=$1
nbu_url=n2psmwindc003.nonprod.abc.com

curl -H "Accept: application/vnd.netbackup+json;version=2.0" -H "Authorization: ${api_key}" -k \
-X GET "https://${nbu_url}/netbackup/admin/jobs?filter=clientName%20eq%20'${clientname}'%20and%20jobType%20eq%20'BACKUP'" | jq . | grep scheduleType


# bash -x nbu.sh p1vseslic0001| jq '.data[].attributes | .scheduleType + " " + .endTime'
