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
 
HOW_LONG = 1
SITESCOPE_PASSWORD=os.environ['SITESCOPE_PASSWORD']


def cal_date(start_suppress):
    from_datetime = datetime.strptime(start_suppress, '%Y%m%d%H%M')
    from_diff = int(from_datetime.timestamp() - datetime.now().timestamp())
    return from_diff
 
 
def check_monitor(host: str, group_name: str, web_URL: str):
    find_url = f'{web_URL}/api/monitors/group/properties'
    params = {'fullPathToGroup': group_name}
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth('administrator', os.environ['SITESCOPE_PASSWORD']))
    output = json.loads(response.text)
    print(f"{host} {output['status']}")


def send_http_request(host: str, api_url: str, params: dict, start_suppress, blackout_duration):
    response = requests.post(api_url, data=params, verify=False, \
                             auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    if host[2] == "p":
        print(f"WARNING: You need to disable NNMI - {host}.")

    if response.status_code == 204:
        print(f"{response.status_code}  {host} {sys.argv[2]} start from {start_suppress} for {blackout_duration/1000} secs.")
    else:
        print(f"{response.status_code}  {host} {sys.argv[2]} Failed.")
 

def get_http_request_params(groups_dict, group_name, host, start_suppress, blackout_duration, 
                            mon_state, web_URL):

    group_url = f'{web_URL}/api/monitors/group/status'
    mon_url = f'{web_URL}/api/monitors/monitor/status'
    params = None
    api_url = None
    desc = None
    from_diff = cal_date(start_suppress) * 1000
    to_diff = from_diff + blackout_duration
    
    if groups_dict[group_name] == 'Group' and host in group_name:
    # Suppress monitoring for 4 hours
        params = {
            'fullPathToGroup': group_name,
            'enable': mon_state,
            'fromTime': str(from_diff),
            'toTime': str(to_diff),
            'description': f"SMAX{desc}"
        }
        api_url = group_url

    if groups_dict[group_name] == 'Monitor' and "DNS Monitor" in group_name \
        and "Ping" not in group_name:
        # Suppress monitoring for 4 hours
        params = {
            'fullPathToMonitor': group_name,
            'enable': mon_state,
            'fromTime': str(from_diff),
            'toTime': str(to_diff),
            'description': f"SMAX{desc}"
        }
        api_url = mon_url

    return params, api_url


def find_items_from_hostname(args: argparse.Namespace, web_URL: str):
    desc = args.desc
    find_url = f'{web_URL}/api/monitors'
    # params = {'name': 'SAUT'} # large group
    params = {
        'entity_type': '', # for both monitors and groups.
        'searchregex': 'true',
        'name': args.hostname
    }
 
    # Find the group name in sitescope
    response = requests.get(find_url, params=params, verify=False, 
                            auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    if response.status_code != 200:
        print("Error: Auth failed.")
        sys.exit(1)
    
    return json.loads(response.text)

 
def main(args: argparse.Namespace):

    blackout_duration = args.length * 180 * 1000
	
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
        web_URL = 'https://n1vsmobmaw0010.nonprod.abc.com/SiteScope'
    else:
        web_URL = 'https://p1vsmobmaw0010.prod.abc.com/SiteScope'

    find_url = f'{web_URL}/api/monitors'
 
    if mon_state != 'check'and not args.time:
        print("Error: no blackout start time.")
        sys.exit(1)
    
    start_suppress = args.time

    groups_dict = find_items_from_hostname(args, web_URL)
 
    # Post to sitescope
    for k, group_name in enumerate(groups_dict):
        if mon_state == 'check':
            if groups_dict[group_name] == 'Group':
                check_monitor(host, group_name, web_URL)
        else:
            if groups_dict[group_name] == 'Group' or "DNS Monitor" in group_name:
                # print(group_name)
                api_url = None
                params = None
                params, api_url = get_http_request_params(groups_dict, group_name, host, 
                                                        start_suppress, blackout_duration, mon_state, web_URL)
                # Send http request
                if api_url:
                    send_http_request(host, api_url, params, start_suppress, blackout_duration)

 
if __name__ == '__main__':
    # response = requests.get('{NP_URL}//api/monitors/snapshots', params=params, verify=False, auth=HTTPBasicAuth('administrator', SITESCOPE_PASSWORD))
    parser = argparse.ArgumentParser(description="Manage sitescope")
    # parser.add_argument('--env', '-e', type=str, help="environment is np / pr")
    parser.add_argument('--action', '-a', type=str, help="action is enable / disable / check")
    parser.add_argument('--hostname', type=str, help="Hostname")
    parser.add_argument('--time', '-t', type=str, help="Suppress Time", required=False)
    parser.add_argument('--desc', '-d', type=str, help="Description", required=False)
    parser.add_argument('--length', '-l', default=1, type=int, help="Blackout length", required=False)
    args = parser.parse_args()
 
    main(args)
