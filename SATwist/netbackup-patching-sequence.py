#!/opt/opsware/bin/python3

import os
import re
import subprocess
import sys

from pytwist import twistserver
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.device import DeviceGroupVO
from pytwist.com.opsware.server import ServerRef


HOST_REBOOT_SEQ = [
    ["n1psmwind0001", "n2psmwind0001"],
    ["n1psmwind0002", "n2psmwind0002"],
    ["n1psmwind0003", "n2psmwind0003"],
    ["n1psmwind0004", "n2psmwind0004"],
    ["n1psmwind0005", "n2psmwind0005"],
    ["n1psmwind0006", "n2psmwind0006"],
    ["n1psmwind0007", "n2psmwind0007"]
]


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


class CommonSettings:
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
            ServerService = ts.server.ServerService
            DGS = ts.device.DeviceGroupService
            ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))
            self.deviceRefs = DGS.getDevices(ref)
            self.deviceRefMap = {}
            for devRef in self.deviceRefs:               
                vo = ServerService.getServerVO(devRef)
                pattern = r'(\w+)\..*'
                match = re.search(pattern, vo.getHostName())
                hostname = match.group(1)
                self.deviceRefMap[hostname] = devRef


    def get_device_ref(self, ts, hostname):

        return self.deviceRefMap


    def get_tmr0000(self):
        import os
        import time
        from datetime import date, datetime, timedelta

        os.environ['TZ'] = 'Asia/Hong_Kong'
        time.tzset()
    
        today = datetime.now()
        tmr = today + timedelta(1)    # Add 1 day from today
        tmr_0000 = datetime.combine(tmr, datetime.min.time()).timestamp()

        return tmr_0000


class PatchedHost:

    def __init__(self, ts, hostname):
        self.ts = ts
        self.hostname = hostname

    def start_to_patch():
        pass


def main():

    ts = auth()
    settings = CommonSettings(ts, "Public/Netbackup/NP")
    a = settings.get_device_ref(ts, "n1psmwind0001")
    print(a)
    # host = PatchedHost(ts, "n1psmwind0001")
    # host.start_to_patch()


if __name__ == '__main__':
    main()
