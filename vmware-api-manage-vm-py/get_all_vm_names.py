#!/usr/bin/env python
"""
Python program for flat text listing the VMs on an
ESX / vCenter, host one per line.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from datacenter import run_cli
from tools import cli, service_instance, pchelper
from pyVmomi import vim

import inspect
import logging

MAX_DEPTH = 10
vmdup = []
vms = []

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(message)s", filemode='w',)

def print_vminfo(vm, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
    with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            print_vminfo(child, depth+1)
        return

    summary = vm.summary
    if summary.config.name in vms:
        vmdup.append(summary.config.name)
    else:
        vms.append(summary.config.name)
    logging.info(summary.config.name)
    # print(summary.config.name)


def get_vms_in_dc(vm_name=None):
    """
    Simple command-line program for listing the virtual machines on a host.
    """

    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)

    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)

    for child in content.rootFolder.childEntity:
        if child == DATACENTER:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmfolder = datacenter.vmFolder
                vmlist = vmfolder.childEntity
                for vm in vmlist:
                    print_vminfo(vm)
    if len(vmdup) > 0:
        print(f"{vmdup} are duplicated in vcenter. Ensure vm name is unique in vcenter.")
    return vmdup

def main():
    get_vms_in_dc()

# Start program
if __name__ == "__main__":
    main()

