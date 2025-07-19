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


HOST_REBOOT_SEQ = [
    ["n1vsmsautw0001", "p2vsmsautw0001"],
    ["p1vsmsautw0001", "p1vsmsautw0002"]
]

os.environ['TZ'] = 'Asia/Hong_Kong'
time.tzset()

WIN_SCRIPT_NAME = "win-reboot-after-patch-install"


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


class PatchAllHostsInDeviceGroup:
    _instance = None  # Class-level variable to hold the single instance


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, ts, smaxsubfolder):

        # __init__ is called every time, but only initializes the first time
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            self._initialized = True
            self.ts = ts
            ServerService = self.ts.server.ServerService
            DGS = self.ts.device.DeviceGroupService
            ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))
            self.deviceRefs = DGS.getDevices(ref)
            self.deviceRefMap = {}
            self.create_device_map()


    def create_device_map(self):
        ServerService = self.ts.server.ServerService
        for devRef in self.deviceRefs:               
                vo = ServerService.getServerVO(devRef)
                pattern = r'(\w+)\..*'
                match = re.search(pattern, vo.getHostName())
                hostname = match.group(1)
                self.deviceRefMap[hostname] = devRef


    def get_device_ref(self, hostname):
        return self.deviceRefMap[hostname]


    def get_tmr0000(self):
        from datetime import date, datetime, timedelta
    
        today = datetime.now()
        tmr = today + timedelta(1)    # Add 1 day from today
        tmr_0000 = datetime.combine(tmr, datetime.min.time()).timestamp()

        return int(tmr_0000)
    

    def schedule_win_patch_install(self, tmr_0000, device_group_path):
        jobSchedule = JobSchedule()
        jobNotification = JobNotification()
        ServerService = self.ts.server.ServerService

        jobSchedule.startDate = tmr_0000 + 28800        # Start to install patch at 9am
        args = ServerScriptJobArgs()
        args.timeOut = 60 * 60
        args.parameters = device_group_path
        SearchService = self.ts.search.SearchService
        args.targets = SearchService.findObjRefs('ServerVO.name = "PCORE1"', 'device')
        scriptRef = SearchService.findObjRefs('ServerScriptVO.name = "xxx-win-install-software"', 'server_script')[0]
        userTag = device_group_path
        ServerScriptService = self.ts.script.ServerScriptService
        jobRef = ServerScriptService.startServerScript(scriptRef, args, userTag, jobNotification, jobSchedule)
        print(f"Created job {jobRef} for patch installtions")


    def reboot_script_ref(self):
        SearchService = self.ts.search.SearchService
        win_scriptRef = SearchService.findObjRefs(f'ServerScriptVO.name = {WIN_SCRIPT_NAME}', 'server_script')[0]
        return win_scriptRef


class RebootHosts:

    def __init__(self, settings, hostnames):
        self.settings = settings
        self.ts = self.settings.ts
        self.targets = []

        for h in hostnames:
            self.targets.append(self.settings.get_device_ref(h))


    def schedule_reboot(self, reboot_time, reboot_script_ref):
        ServerScriptService = self.ts.script.ServerScriptService
        jobSchedule = JobSchedule()
        jobNotification = JobNotification()
        jobSchedule.startDate = reboot_time
        args = ServerScriptJobArgs()
        args.timeOut = 60 * 60
        args.targets = self.targets
        userTag = f"smax"
        jobRef = ServerScriptService.startServerScript(reboot_script_ref, args, userTag, jobNotification, jobSchedule)
        print(jobRef)
        
        return reboot_time + 1200


def main():

    ts = auth()
    settings = PatchAllHostsInDeviceGroup(ts, "Public/Test/NP")
    tmr_0000 = settings.get_tmr0000()
    reboot_script_ref = settings.reboot_script_ref() 
    # tmr_0000 = int(time.time())
    # Install patch time
    settings.schedule_win_patch_install(tmr_0000, "Public/Test/NP")

    reboot_time = tmr_0000 + 39600
    for index, hosts in enumerate(HOST_REBOOT_SEQ):
        res = RebootHosts(settings, hosts)
        reboot_time = res.schedule_reboot(reboot_time, reboot_script_ref)


if __name__ == '__main__':
    main()

