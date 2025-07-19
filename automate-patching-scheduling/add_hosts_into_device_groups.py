#!/opt/opsware/bin/python3

import os
import re
import subprocess
import sys

from pytwist import twistserver
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.device import DeviceGroupVO
from pytwist.com.opsware.server import ServerRef


LNX_SCRIPT_NAME = "yum-update-reboot"
WIN_SCRIPT_NAME = "win-reboot-after-patch-install"


def attach_scripts(ts, smaxsubfolder, linux_scriptRef, win_scriptRef):

    from pytwist.com.opsware.job import JobNotification, JobSchedule
    from pytwist.com.opsware.script import ServerScriptJobArgs
    from datetime import date, datetime, timedelta
    
    email = 'pccwshkprojectlifeinfrasystem@pccw.com'
    jobNotification = JobNotification()
    jobNotification.onCancelRecipients=[email]
    jobNotification.onFailureRecipients=[email]
    jobNotification.onSuccessRecipients=[email]
    #jobSchedule = JobSchedule()

    ServerScriptService = ts.script.ServerScriptService

    import os
    import time

    os.environ['TZ'] = 'Asia/Hong_Kong'
    time.tzset()
 
    args = ServerScriptJobArgs()
    args.timeOut = 4 * 60
 
    #linux_hosts = []
    #win_hosts = []

    today = datetime.now()
    tmr = today + timedelta(1)
    tmr_0000 = datetime.combine(tmr, datetime.min.time()).timestamp()
    #jobSchedule.startDate = int(tmr_0000)

    ServerService = ts.server.ServerService
    DGS = ts.device.DeviceGroupService
    ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))
    children = DGS.getChildren(ref)
    for n, child in enumerate(children):
        linux_hosts = []
        win_hosts = []
        child_dg_name = DGS.getDeviceGroupVO(child)
        exec_time = int(child_dg_name.shortName) / 100
        if exec_time > 8:
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
        jobSchedule.startDate = int(tmr_0000) + int(exec_time)
        userTag = 'run script on servers'
        if linux_hosts:
            args.targets = linux_hosts
            jobRef = ServerScriptService.startServerScript(linux_scriptRef, args, userTag, jobNotification, jobSchedule)
        if win_hosts:
            args.targets = win_hosts
            jobRef = ServerScriptService.startServerScript(win_scriptRef, args, userTag, jobNotification, jobSchedule)
                

def auth():
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization, hashes


    with open('/root/.SA/priv.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    password = b'8\xb5zdG\x1d\xa9\xa9y\xc2:^2p\x92O\xab\x00P\xbf\xaa\x9d4\x12v\xa5\x81mU,\tBo\x1e{\xd8\xac\xe5\x0c\xd9Q`<"\xb8\xd0\xed\x18\xa5\xd8\xbfn\xf1\xa1\x94\xd93{Q\xf9P3\xce\xf6\xb2V\x16\x06\x81\xe5\x98\x0ewE\xc0>\x95Z\x1d~\x9b@4\xbf\xdf\xa245_\x17\x83-\x9f\x0c\xb1\xb4nFa\xe2\x8f\xb5\x89\x83\x96\xee1\xb6\x87\xe0b\\\x07\xa6\x96\xfcg\xba\xc7\xb5f\x1ff\x95\xf1\xe3,I\xfdO!r\x8a\xbf\xa9\xd0\xf5T\x15U<\xeaL\xc6\xc3\xac\xd39$\x04<\xaa\x04<\xa4P[\xaag\xf7|\x86T\x11\x8b\x9d\x89\xff|\xbe\x06M\x9aDk\xdf\xc3e0\xc4kG\xf8^\xcc\xa8\xb8H\x83I\x93\xfbz^XjQ\xd6\xc4\xa4\x17\x9cEv\xb4\xed\xb5\xe0\xbf\xf0&\x86\xd6\x9aP\xab\xedH\xe8\\;rC\xc5ogy\xef\xb3,Q\x14\xe8\\\xe6H\xc7a\x91\x8b\xda\xa8\xf4\xd5\xf4\x80s\xa3F-O\xaa\xa5"\x04\xa0'
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


def read_schedule_csv():
    ## Read patch info
    smax_num = None
    hosts = []
    serverRef = []
    try:
        with open('/tmp/servers.csv') as f:
            for index, line in enumerate(f):
                if index == 0 and line[0] == '#':
                    line = line.replace('#', '')
                    line = line.replace(' ', '')
                    smax_num = line.strip()
                elif index == 0 and line[0] != '#':
                    # ignore all comments # besides the first
                    print("Error: format problem in /tmp/servers.csv")
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

    smax_num, hosts = read_schedule_csv()
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

    SearchService = ts.search.SearchService
    linux_scriptRef = SearchService.findObjRefs(f'ServerScriptVO.name = {LNX_SCRIPT_NAME}', 'server_script')[0]
    
    win_scriptRef = SearchService.findObjRefs(f'ServerScriptVO.name = {WIN_SCRIPT_NAME}', 'server_script')[0]

    # Attach the scripts to hosts with schedule
    attach_scripts(ts, f"Public/SMAX/{smax_num}", linux_scriptRef, win_scriptRef)


sys.exit(0)
