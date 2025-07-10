#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The script is used to query the nbu
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


NBU_SERVERs = {
    "p1": "p1psmwindc003.prod.abc.com",
    "p2": "p2psmwindc003.prod.abc.com",
    "n1": "n1psmwindc003.nonprod.abc.com",
    "n2": "n2psmwindc003.nonprod.abc.com",
}

class NBUClient:
    def __init__(self, hostname):
        self.hostname = hostname

    
    def call_server(self):
        nbu_s = NBU_SERVERs[self.hostname[0:2]]
        api_key = os.environ.get(f"{self.hostname[0:2]}_nbu_api")
        headers = {
            "Authorization": api_key,
            "Accept": "application/vnd.netbackup+json;version=2.0"
        }
        params = {
            "filter": f"clientName eq '{self.hostname}' and jobType eq 'BACKUP'",
            "page[limit]": 14
        }
        response = requests.get(f"https://{nbu_s}/netbackup/admin/jobs", params=params, 
                                headers=headers, verify=False)
        output = json.loads(response.text)
        for item in output["data"]:
            print(f'{self.hostname} {item["id"]:7s} {item["attributes"]["scheduleType"]:25s} {item["attributes"]["endTime"][0:10]:10s} {item["attributes"]["state"]}')

        print("=========")
        print("*********")


def main(args):
    n = NBUClient(args.hostname)
    n.call_server()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Query NBU")
    parser.add_argument('--hostname', type=str, help="hostname", required=True)
    args = parser.parse_args()
    main(args)
