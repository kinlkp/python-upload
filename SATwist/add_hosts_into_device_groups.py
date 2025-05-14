#!/opt/opsware/bin/python

import sys

from pytwist import twistserver
from pytwist.com.opsware.search import Filter
from pytwist.com.opsware.device import DeviceGroupVO
from pytwist.com.opsware.server import ServerRef


def auth():
    ## Connect to SA
    ts = twistserver.TwistServer()
    ts.authenticate("admin","S@isfunn!2025")
    return ts


def read_csv():
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
                    smax_num = line
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
    smax_num, hosts = read_csv()
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
        start_time = h_arr[1]
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
        start_time = h_arr[1]
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

sys.exit(0)
