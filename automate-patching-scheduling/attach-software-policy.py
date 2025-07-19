#!/opt/opsware/bin/python


import time
import sys
from pytwist import twistserver
from pytwist.com.opsware.job import JobNotification, JobSchedule
from pytwist.com.opsware.swmgmt import PolicyAttachableMap, PolicyRemediateJobArgument, AnalyzeArgument, StageArgument, ActionArgument, SoftwareInstallJobArgument, InstallableAttachableEntry


WIN_POLICY = "win-patch-202505"


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


def findRefs(ts, filt, obj):
    refs = ts.search.SearchService.findObjRefs(filt, obj)
    if not refs:
        print("%s not found" % obj)
        sys.exit(1)
    return refs


def main():

    import sys
    from pytwist import twistserver
    from pytwist.com.opsware.swmgmt import PolicyAttachableMap, PolicyRemediateJobArgument, AnalyzeArgument, StageArgument, ActionArgument

    smaxsubfolder = sys.argv[1].strip()
    
    win_hosts = []

    ts = auth()

    SPP = ts.swmgmt.SoftwarePolicyService

    DGS = ts.device.DeviceGroupService
    ref = DGS.getDeviceGroupByPath(smaxsubfolder.split('/'))

    ServerService = ts.server.ServerService
    for devRef in DGS.getDevices(ref):
        vo = ServerService.getServerVO(devRef)
        if "NT" in vo.osVersion:
            # print("win")
            win_hosts.append(devRef)

    if win_hosts:
        policyRefs = findRefs(ts, f'SoftwarePolicyVO.name = "{WIN_POLICY}"','software_policy')

        SPP.attachToPolicies(policyRefs, win_hosts)

        pam = PolicyAttachableMap()
        pam.attached = True  # we've call attachToPolicies already
        pam.policies = policyRefs
        pam.policyAttachables = win_hosts

        prja = PolicyRemediateJobArgument()
        prja.policyAttachableMap = [pam]
        prja.ticketId = f"{WIN_POLICY}"
        prja.analyzePhaseArguments = AnalyzeArgument()
        prja.stagePhaseArguments = StageArgument()
        prja.actionPhaseArguments = ActionArgument()
        prja.expandAtRuntime = True

        SPP.startRemediate(prja)
    else:
        print("No Windows")


if __name__ == '__main__':
    main()

