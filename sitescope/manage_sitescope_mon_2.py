#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The script is used to suppress the sitescope monitoring
"""
 
import argparse
import datetime
import json
import requests
import sys
import os
import urllib3
 
from datetime import datetime
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
 
 
disable_warnings(InsecureRequestWarning)
 
   
SITESCOPE_PASSWORD = os.environ['SITESCOPE_PASSWORD']

 
def cal_date(start_suppress):
    from_datetime = datetime.strptime(start_suppress, '%Y%m%d%H%M')
    from_diff = int(from_datetime.timestamp() - datetime.now().timestamp())
    return from_diff
 
 
def check_monitor(host: str, group_name: str, web_URL: str):
    find_url = f'{web_URL}/api/monitors/group/properties'
    params = {'fullPathToGroup': group_name}
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth(os.environ['SITESCOPE_USER'], SITESCOPE_PASSWORD))
    output = json.loads(response.text)
    print(f"{host} {output['status']}")
 
 
def main(args: argparse.Namespace):
    blackout_duration = 1 * 3300 * 1000
    if args.action == 'enable':
        mon_state = 'true'
    elif args.action == 'disable':
        mon_state = 'false'
    else:
        mon_state = 'check'
 
    host = args.hostname
    if not host:
        print("Error: no hostname provides.")
        sys.exit(1)

    if host[0] == 'n':
        web_URL = 'https://n1vsmobmaw0010.nonprod.empf.local/SiteScope'
    else:
        web_URL = 'https://p1vsmobmaw0010.prod.empf.local/SiteScope'

    find_url = f'{web_URL}/api/monitors'
    set_url = f'{web_URL}/api/monitors/group/status'
 
    if args.time:
        start_suppress = args.time

    # if not args.desc:
    #     print("Error: No description.")
    #     sys.exit(1)

    desc = args.desc
    # params = {'name': 'SAUT'} # large group
    params = {
        'entity_type': '', # for both monitors and groups.
        'searchregex': 'true',
        'name': host
    }
 
    # Find the group name in sitescope
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    if response.status_code != 200:
        print("Error: Auth failed.")
        sys.exit(1)
    groups_dict = json.loads(response.text)
 
    # Post to sitescope
    for k, group_name in enumerate(groups_dict):
        if groups_dict[group_name] == 'Group' and host in group_name:
            if mon_state == "check":
                check_monitor(host, group_name, web_URL)
                break
            # Suppress monitoring for 4 hours
            from_diff = cal_date(start_suppress) * 1000
            to_diff = from_diff + blackout_duration
            params = {
                'fullPathToGroup': group_name,
                'enable': mon_state,
                'fromTime': str(from_diff),
                'toTime': str(to_diff),
                'description': f"SMAX{desc}"
            }
            response = requests.post(set_url, data=params, verify=False, 
                                     auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
            if response.status_code == 204:
                print(f"{response.status_code}  {host} {sys.argv[2]} start from {start_suppress} for {blackout_duration/1000} secs.")
            else:
                print(f"{response.status_code}  {host} {sys.argv[2]} Failed.")
            break
 
 
if __name__ == '__main__':
    # response = requests.get('{NP_URL}//api/monitors/snapshots', params=params, verify=False, auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    parser = argparse.ArgumentParser(description="Manage sitescope")
    # parser.add_argument('--env', '-e', type=str, help="environment is np / pr")
    parser.add_argument('--action', '-a', type=str, help="action is enable / disable / check")
    parser.add_argument('--hostname', type=str, help="hostname")
    parser.add_argument('--time', '-t', type=str, help="Suppress Time", required=False)
    parser.add_argument('--desc', '-d', type=str, help="Description", required=False)
    args = parser.parse_args()
 
    main(args)
    # check_monitor()
