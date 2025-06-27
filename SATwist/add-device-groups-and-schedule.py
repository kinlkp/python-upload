#!/opt/opsware/bin/python3

import os
import re
import subprocess
import sys
import time

from pytwist import twistserver
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.device import DeviceGroupVO
from pytwist.com.opsware.server import ServerRef

from pytwist.com.opsware.job import JobNotification, JobSchedule
from pytwist.com.opsware.script import ServerScriptJobArgs
from datetime import date, datetime, timedelta


LNX_SCRIPT_NAME = "yum-update-reboot"
WIN_SCRIPT_NAME = "win-reboot-after-patch-install"


def schedule_to_check_patch(ts, smax_num, tmr_0000):
    DGS = ts.device.DeviceGroupService
    SearchService = ts.search.SearchService
    ServerService = ts.server.ServerService
    ServerScriptService = ts.script.ServerScriptService

    ref = DGS.getDeviceGroupByPath(f"Public/SMAX/{smax_num}".split('/'))
    children = DGS.getChildren(ref)
    for n, child in enumerate(children):
        linux_hosts = []
        win_hosts = []
        child_dg_name = DGS.getDeviceGroupVO(child)
        time_folder_name = child_dg_name.shortName[0:2].strip()

        for devRef in DGS.getDevices(child):
            vo = ServerService.getServerVO(devRef)
            if "Linux" in vo.osVersion:
                # print("linux")
                linux_hosts.append(devRef)
            if "NT" in vo.osVersion:
                # print("win")
                win_hosts.append(devRef)

        
        jobNotification = JobNotification()
        jobSchedule = JobSchedule()

        jobSchedule.startDate = int(tmr_0000) + 32400   # checking starts at 9am
        linux_scriptRef = SearchService.findObjRefs('ServerScriptVO.name = "3_healthcheck-after-yum-update"', 'server_script')[0]
        win_scriptRef = SearchService.findObjRefs('ServerScriptVO.name = "check-after-win-patching"', 'server_script')[0]
        args = ServerScriptJobArgs()
        args.timeOut = 60 * 60

        args.targets = DGS.getDevices(child)
        userTag = f"smax {smax_num}"
        ServerScriptService.startServerScript(linux_scriptRef, args, userTag, jobNotification, jobSchedule)

        ServerScriptService.startServerScript(win_scriptRef, args, userTag, jobNotification, jobSchedule)



def schedule_to_install_software(ts, reboot_time, smaxsubfolder, jobNotification):
    jobSchedule = JobSchedule()
    ServerService = ts.server.ServerService
    jobSchedule.startDate = int(reboot_time) - 10800
    #jobSchedule.startDate = int(time.time()) + 5
    args = ServerScriptJobArgs()
    args.timeOut = 10 * 60
    args.parameters = f"{smaxsubfolder}"
    args.targets = SearchService.findObjRefs('ServerVO.name = "PCORE1"', 'device')
    scriptRef = SearchService.findObjRefs('ServerScriptVO.name = "schedule-win-install-software"', 'server_script')[0]
    userTag = f"smax {smaxsubfolder.split('/')[-2]}"
    ServerScriptService = ts.script.ServerScriptService
    jobRef = ServerScriptService.startServerScript(scriptRef, args, userTag, jobNotification, jobSchedule)
    print(f"Created job {jobRef}")


def attach_scripts(ts, smaxsubfolder, linux_scriptRef, win_scriptRef):
    
    #email = 'pccwshkprojectlifeinfrasystem@pccw.com'
    jobNotification = JobNotification()
    #jobNotification.onCancelRecipients=[email]
    #jobNotification.onFailureRecipients=[email]
    #jobNotification.onSuccessRecipients=[email]

    ServerScriptService = ts.script.ServerScriptService

    import os
    import time

    os.environ['TZ'] = 'Asia/Hong_Kong'
    time.tzset()
 
    args = ServerScriptJobArgs()
    args.timeOut = 60 * 60
 
    today = datetime.now()
    tmr = today + timedelta(1)    # Add 1 day from today
    tmr_0000 = datetime.combine(tmr, datetime.min.time()).timestamp()

    ServerService = ts.server.ServerService
    DGS = ts.device.DeviceGroupService
    ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))
    children = DGS.getChildren(ref)
    for n, child in enumerate(children):
        linux_hosts = []
        win_hosts = []
        child_dg_name = DGS.getDeviceGroupVO(child)
        time_folder_name = child_dg_name.shortName[0:2].strip()
        exec_time = int(time_folder_name)
        if exec_time > 8:
            print("Error: time is over 8am.")
            sys.exit(1)
        exec_time = exec_time * 3600
        print(exec_time)
        for devRef in DGS.getDevices(child):
            vo = ServerService.getServerVO(devRef)
            if "Linux" in vo.osVersion:
                # print("linux")
                linux_hosts.append(devRef)
            if "NT" in vo.osVersion:
                # print("win")
                win_hosts.append(devRef)

        jobSchedule = JobSchedule()
        reboot_time = int(tmr_0000) + int(exec_time) + 180
        jobSchedule.startDate = reboot_time
        userTag = f"smax {smaxsubfolder.split('/')[-1]}"
        if linux_hosts:
            args.targets = linux_hosts
            jobRef = ServerScriptService.startServerScript(linux_scriptRef, args, userTag, jobNotification, jobSchedule)
        if win_hosts:
            args.targets = win_hosts
            jobRef = ServerScriptService.startServerScript(win_scriptRef, args, userTag, jobNotification, jobSchedule)
            schedule_to_install_software(ts, reboot_time, f"{smaxsubfolder}/{child_dg_name.shortName.strip()}", jobNotification)
    
    return int(tmr_0000)
          

def auth():
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization, hashes

    # Get the private from server
    with open('/root/.SA/priv.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    password = b'8\xb5zdG\x1d\xa9\xa9y\xc2:^2p\x92O\xab\x00P\xbf\xaa\x9d4\x12v\xa5\x81mU,\tBo\x1e{\xd8\xac\xe5\x0c\xd9Q`<"\xb8\xd0\xed\x18\xa5\xd8\xbfn\xf1\xa1\x94\xd93{Q\xf9P3\xce\xf6\xb2V\x16\x06\x81\xe5\x98\x0ewE\xc0>\x95Z\x1d~\x9b@4\xbf\xdf\xa245_\x17\x83-\x9f\x0c\xb1\xb4nFa\xe2\x8f\xb5\x89\x83\x96\xee1\xb6\x87\xe0b\\\x07\xa6\x96\xfcg\xba\xc7\xb5f\x1ff\x95\xf1\xe3,I\xfdO!r\x8a\xbf\xa9\xd0\xf5T\x15U<\xeaL\xc6\xc3\xac\xd39$\x04<\xaa\x04<\xa4P[\xaag\xf7|\x86T\x11\x8b\x9d\x89\xff|\xbe\x06M\x9aDk\xdf\xc3e0\xc4kG\xf8^\xcc\xa8\xb8H\x83I\x93\xfbz^XjQ\xd6\xc4\xa4\x17\x9cEv\xb4\xed\xb5\xe0\xbf\xf0&\x86\xd6\x9aP\xab\xedH\xe8\\;rC\xc5ogy\xef\xb3,Q\x14\xe8\\\xe6H\xc7a\x91\x8b\xda\xa8\xf4\xd5\xf4\x80s\xa3F-O\xaa\xa5"\x04\xa0'
    # Decrypt the password using private key
    decrypted = private_key.decrypt(
        password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    password = decrypted.decode()

    ## Connect to SA
    ts = twistserver.TwistServer()
    ts.authenticate('admin', password)
    return ts


def read_servers_csv():

    # Download the servers.csv from p2vsmsautl0010
    download_command='http_proxy="" curl http://10.122.0.21:3001/sasa/servers.csv -o /tmp/servers.csv 2>/tmp/null'
    os.system(download_command)

    ## Read patch info
    smax_num = None
    hosts = []
    serverRef = []
    try:
        with open('/tmp/servers.csv', "r") as f:
            for index, line in enumerate(f):
                if index == 0 and line[0] == '#':
                    line = line.replace('#', '')
                    line = line.replace(' ', '')
                    smax_num = line.strip()
                elif index == 0 and line[0] != '#':
                    # ignore all comments # besides the first
                    print("Error: format problem in /tmp/servers.csv")
                    print("# smax-number")
                    print("host1,0000-0200")
                    sys.exit(1)
                elif index != 0 and line[0] == '#':
                    # skip the line
                    continue
                else:
                    hosts.append(line.strip())
    except:
        print("Error: failed to open /tmp/servers.csv")
        sys.exit(1)

    if not smax_num:
        print("Error: No SMAX number.")
        sys.exit(1)
    return smax_num, hosts


if __name__ == '__main__':

    # Read servers.csv from http://10.122.0.21:3001/sasa/servers.csv
    smax_num, hosts = read_servers_csv()

    # Create the device group for SMAX
    root = "Public/SMAX"
    ts = auth()

    DGS = ts.device.DeviceGroupService
    try:
        ref = DGS.getDeviceGroupByPath(root.split('/'))
    except NotFoundException:
        print('Path "%s" not found' % root)
        sys.exit(1)
    vo = DeviceGroupVO()
    vo.parent = ref
    vo.shortName = smax_num
    newVO = DGS.create(vo)

    # Create the device groups for timeslots
    for h in hosts:
        h_arr = h.split(',')
        start_time = h_arr[1].replace(" ","")
        start_time = re.sub('\-.*$', '', start_time).strip()
        newroot = f"Public/SMAX/{smax_num}"
        ref = DGS.getDeviceGroupByPath(newroot.split('/'))
        vo = DeviceGroupVO()
        vo.parent = ref
        vo.shortName = start_time
        try:
            DGS.getDeviceGroupByPath(f"Public/SMAX/{smax_num}/{start_time}".split('/'))
        except:
            newVO = DGS.create(vo)

    for h in hosts:
        h_arr = h.split(',')
        hostname = h_arr[0]
        start_time = h_arr[1].replace(" ","")
        start_time = re.sub('\-.*$', '', start_time).strip()
        ServerService = ts.server.ServerService
        ## Create filter to find the host
        f = Filter()
        f.expression = f'ServerVO.hostName *=* "{hostname}"'
        foundServers = ServerService.findServerRefs(f)
        if foundServers:
            print(foundServers)
            #serverRef.append(foundServers[0])
        smaxsubfolder = f"Public/SMAX/{smax_num}/{start_time}"
        ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))
        #print(type(ref))
        DGS.addDevices(ref,foundServers)

    # Search the scripts
    SearchService = ts.search.SearchService
    linux_scriptRef = SearchService.findObjRefs(f'ServerScriptVO.name = {LNX_SCRIPT_NAME}', 'server_script')[0]
    
    win_scriptRef = SearchService.findObjRefs(f'ServerScriptVO.name = {WIN_SCRIPT_NAME}', 'server_script')[0]

    # Attach the scripts to hosts with schedule
    tmr_0000 = attach_scripts(ts, f"Public/SMAX/{smax_num}", linux_scriptRef, win_scriptRef)

    # Schedule the checking
    schedule_to_check_patch(ts, smax_num, tmr_0000)

    # Remove /tmp/servers.csv
    os.unlink('/tmp/servers.csv')

sys.exit(0)

