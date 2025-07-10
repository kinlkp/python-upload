#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The script is used to suppress the sitescope monitoring
"""
import datetime
import json
import requests
import sys
import os
# import urllib3


from datetime import datetime
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings


disable_warnings(InsecureRequestWarning)

   
SITESCOPE_PASSWORD = os.environ['SITESCOPE_PASSWORD']

NP_URL = 'https://p1vsmobmaw0010.prod.abc.com/SiteScope'

if not sys.argv[4]:
            print("Error: date/time is not provided.")
            sys.exit()
start_suppress = sys.argv[4]


def cal_date(start_suppress: str):
    from_datetime = datetime.strptime(start_suppress, '%Y%m%d%H%M')
    from_diff = int(from_datetime.timestamp() - datetime.now().timestamp())
    return from_diff


def check_monitor(host: str, group_name: str):
    find_url = f'{NP_URL}/api/monitors/group/properties'
    params = {'fullPathToGroup': group_name}
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth(os.environ['SITESCOPE_USER'], SITESCOPE_PASSWORD))
    output = json.loads(response.text)
    print(f"{host} {output['status']}")


def main():
    if sys.argv[1] == 'np':
        find_url = f'{NP_URL}/api/monitors'
        set_url = f'{NP_URL}/api/monitors/group/status'

    if sys.argv[2] == 'enable':
        mon_state = 'true'
    elif sys.argv[2] == 'disable':
        mon_state = 'false'
    else:
        mon_state = 'check'

    host = sys.argv[3]
    if not host:
        print("Error: no hostname provides.")
        sys.exit(1)

    # params = {'name': 'SAUT'} # large group
    params = {
        'name': host
    }
    # Find the group in sitescope
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    groups_dict = json.loads(response.text)

    # Suppress monitoring for 4 hours
    from_diff = cal_date(start_suppress) * 1000
    to_diff = from_diff + 28800000

    # Post to sitescope
    for k, group_name in enumerate(groups_dict):
        if groups_dict[group_name] == 'Group' and host in group_name:
            params = {
                'fullPathToGroup': group_name, 
                'enable': mon_state,
                'fromTime': str(from_diff),
                'toTime': str(to_diff)
            }
            if mon_state == "check":
                check_monitor(host, group_name)
                break
            response = requests.post(set_url, data=params, verify=False, 
                                     auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
            if response.status_code == 204:
                print(f"{response.status_code}  {host} {sys.argv[2]} Done from {start_suppress}.")
            else:
                print(f"{response.status_code}  {host} {sys.argv[2]} Failed.")
            break


if __name__ == '__main__':
    # response = requests.get('{NP_URL}//api/monitors/snapshots', params=params, verify=False, auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    main()
    # check_monitor()
