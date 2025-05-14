#!/usr/bin/env python

# Script to operte VM on oVirt thru API

import argparse
import json
import os
import sys

from api_libs.auth import Auth
from api_libs.ovirtvm import oVirtVM
from api_libs.ovirtstorage import oVirtStorage, oVirtStorageSnapshot


def check_args():
    # Open arguement choices file
    # with open("choices.json") as c:
    #     choices = json.load(c)
    parser = argparse.ArgumentParser(description='Operate oVirt commands')
    parser.add_argument('--vm', required=False)
    parser.add_argument('--storage_domain', required=False)
    parser.add_argument('--storage_snapshot', required=False)
    parser.add_argument('--action', required=True)

    return parser.parse_args()


def main():
    if not os.environ.get('OLVM_FQDN'):
        print("Error: environment OLVM_FQDN does not exist.")
        sys.exit()
        
    # Get the oAuth access token
    acces_token = Auth.authenticate()
    args = check_args()
    vm_name = args.vm
    storage_name = args.storage_domain
    storage_snapshot = args.storage_snapshot
    action = args.action
    if vm_name:
        v = oVirtVM(vm_name, action, acces_token)
        v.exec_task()
    elif storage_name:
        v = oVirtStorage(storage_name, action, acces_token)
        v.exec_task()
    elif storage_snapshot:
        v = oVirtStorageSnapshot(storage_snapshot, action, acces_token)
        v.list()
    else:
        print('Error: no object selected. Run "main.py -h"')
  
    
if __name__ == "__main__":
    main()
