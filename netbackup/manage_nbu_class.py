#!/usr/bin/python3.9
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


desc = None


class NBUClient:

    ENC_NBU_API_KEYs = {
        "n1": b"\x19\xb9N:GX\xefY\xb1\xca\xf1\xc8\xbf\xf4r\xf3MP\xde\xbco\xcaZQ0\x06\xf2\x9b\x18\x0f\xf5\x15\x14$*\x93\xc0h\xe0@\x01g\xa7\x06\x108\xbd\r\xadAg\xdb\x91\r\xf9\xab\x12R\xf9\n~\x99\x0eBt|\n<8o\x99\xe2\xd5\xfd\xd6\xfbG^\xe1i\x03xe\x10\xce^\xfc.\xce\x06\xeaE\x16\xf38z\xd6\x1e\xa5\x1f\xa7g\x19\rZ\xe6\x0cG\x84\xa6\x17\xff\x12\xf2\x07\xd2\xe8\x1a\xe35\xaeo^^\x10\x9f\xe8\xe3\x88\x84d\xe7\xedz\xa9n\x9b=\xa3\xb0h\x90\x81\x9c\xab\xaf~\xab\x04\x96\x04\xaa\xab<:\x089?\x88\x8d~4\xe8[\xb4\x95\xf8\xf9\x9e\xf6`\x1cu\xd8\x84nP\xde\x0f\x87\xd5X\xa4\xbe\x14\xa3\xdb\xe4'X\x87\xac\xdc;\xd7\xc1cg\xe1\xc3W\x00QYi\x17\xe5\xbd*\x08}'^\xcd=\xe5\xa7kx\xc0&A\x89\xff=\xf0\xcd\xd2\x96\x16\xfa6c#\xb8\xdcpe)K\xa7\x86\xcb1\\\x1c\xb4\x9c\x8a\x94\t\xe7C\xcbf\xde",
        "p1": b'\x14\xde\x0c9\xd6\xdd\xfe\xf4\x1c\xb6\xff\x913\x10\xef\'\xf5\x8e\x8b\xc1y\xe0\xc6\x10\xc1\x08%=n\x84|\xd9\xdb\xa3\x8e\x17\xd5u8D\xddjn\x1c\xb5\x05\xcb\xb3]q.z\xd1\xd7\x1f~\xa5YQ\x93`\x15\xc8\x9cm\x94\x95\xddG\xa9K\x9b\xa5{L\xb0\xcaf\x0e\x9e\x85\xfflGQ\xfc\xa8j\x12f\xa4z\xbb\x81y\xb9l\xf7c\xa3wr\x03|=\xe7V\xa9}\x83\xd9E\xcc?!Q\x82\xef\xbb&\x01\x9d\x84n\x86.\x12\xf0Oy\xc2og\x1a\tV\x8cR(\x8f\x9f\x9a\x12\x9c\xa0^\xf0\xbe\xa8\x89i*\xf8K\x99\x02\xbd\xed\xb8m\x84\x864\x86\x81\xf6\xdc\xea\xa0\x08X\xfc\xe3\xf7\x01\xa5\xde_ak\x80\xf7w\xa0\xf2;\xfc\x89:\xab&\xb3&a{\xa0\xe19\x9c.b\xbd"e\x0fE\x0b\xdf\xe3_\xf3_\xb6\x10>\xa2\xf4\xc0\xa6\xdf#\x85\x98\xb2r\xf8(\x12&\xbce\xae\x0b\xe3*BZ\x8e\xf4.\xec\x1c\x9c-^\x03L>\x96\x87l\xdcNUD\xd3',
        "p2": b'\xb1X\xcf\x9e\x8d\xd0jo\xfa]L\xe5%\xa3\xeaO\xf2\x1f\x91\xcc4\xe8\xeeg(\x01\x0f\xef\xd5]\xff\xd56\xfbb@\xfe\xde\xb8\xd8>P(EkY\'\x82\x84\x92\x16\xbfC\xaf\x01DX\xed]\x9d\x84\xe0\x8d\x08\xec"gv\xc6R`\xa75\xddj\x16w,\xa74\xfe>\xb5\x8a\xebn\x8f\x1c\x0bI\xac\xbb\x8ac\xad>\x18Nn_\xb9\x06=\xd2\x12\xbd\x0b\xa7X\xc4)\xec\xad\xdb\x98e\x93\xec\xe8!\x97\x07\xe5\xa4,\xce\xa5\xc5\x8cX\x16\x9bF\xb1?!\xc0\xf2\xa0\x8c[\xe1|1\x96^B\xf2\xf7\x039\xf1\x8b\t\x96/)\x864\x19\xea`\x9e\x0c\xe4\x9a<\x03\x96\xf1M\xa3\x17\xd1\x1a5\r\x9c\x8a\x94F\x87hnV\x86\xaa\xfbM\xc0\x1et\x0e\xd3\xaa\x14ao\x97\xa6\xb3\x9e\xcfG\xe1R\x1f\xf5\x03\xc1e\xe3\xee\xd3\x0e\xa9\xdd4\xe6\xb6\xa0\x91\xf2L.\x90H\x0e\x93\xf9s?m@s9h\xa99\xe8\x179h\x03\xfc\xfaF\xc6\x1eI1{\xdf\x01\x89\xb6',
        "n2": b'\r6\xbc\x17\xa3\xe1\x14\xdb\r\xef=\xa1P(\x82\xee!F\xf9\x86\x7f4\x14\xaf\xc9K$:\x9b\xc4\x00\xcb\xd2mZ\xd4\x8a\xde\xe6P\xc1\xd8\xb4R\x16\x1e\x99"yR\xd1\xf9q\xe9\x8f39z\x96\x1bOq=\xe6QD\xe6l~\x8d_ \x98vu6\x9fl\x19\xd1\xdc\x8a[\x02\xd7FB.\x01\xe5\x1fBvy\xb1f\xfcwmo\x98\x98\xda\x81\xda\x869\x8c\xb43\x18d\x14"2\xa5`8\x84\x94\x91\xe7l\x1b}\x05\x0c\x1c\xa2"\x15G*r5lv\r\xaa\xf8\x9cy\xc6\xe9\xc1o\x8d\xeb\xa5\xe0\xa1\x15\x19\xd0\xceI\x05\xe9\x8a5&\xbag\xa1\x7f\xb1\x9e\x16\x01\x14\xdd^a\x8f#\x84j\xe5u\xac/j\x1e\xcbq\x90\'\xd7\x19\x89K\xc6\x9b\x17u\x9f\x0cE\xb2\xc8=\x99fl\xec\\\xdd\xed`\x82\xfd\xe6\x81\x8dx\xed\x85\xd9\xd9?Z\x11;\xd2\xf1\x9e\x1a\x88\x00\xce\xab1\x12\x8f\n)\xc6}x\\\xb6\xba\x9asr\xe9#\xc5E\x90;\xf4[\xfe\xc0T'
    }

    NBU_SERVERs = {
        "p1": "p1psmwindc003.prod.empf.local",
        "p2": "p2psmwindc003.prod.empf.local",
        "n1": "n1psmwindc003.nonprod.empf.local",
        "n2": "n2psmwindc003.nonprod.empf.local",
    }


    def __init__(self, row):
         host, _ = row.split(',')
         if not host:
             print("Error: no hostname provides.")
             sys.exit(1)
         self.hostname = host


    def get_password(self, nbu_env):
        from cryptography.hazmat.primitives.asymmetric import rsa, padding
        from cryptography.hazmat.primitives import serialization, hashes
        # Get the private from server
        with open('/root/.sitescope/priv.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        # Decrypt the password using private key
        decrypted = private_key.decrypt(
            NBUClient.ENC_NBU_API_KEYs[nbu_env],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        password = decrypted.decode()
        return password
        

    def call_server(self):
        nbu_env = self.hostname[:2]     # for example, n1, n2, p1, p2
        import socket
        this_host = socket.gethostname()
        if nbu_env[0] != this_host[0]:
            # print(f'{self.hostname} is not in this nbu.')
            return
        nbu_s = NBUClient.NBU_SERVERs[nbu_env]
        headers = {
            "Authorization": self.get_password(nbu_env),
            "Accept": "application/vnd.netbackup+json;version=2.0"
        }
        params = {
            "filter": f"clientName eq '{self.hostname}' and jobType eq 'BACKUP'",
            "page[limit]": 5
        }
        response = requests.get(f"https://{nbu_s}/netbackup/admin/jobs", params=params, headers=headers, verify=False)

        output = json.loads(response.text)
        try:
            for item in output["data"]:
                #print(f'{self.hostname} {item["id"]:7s} {item["attributes"]["scheduleType"]:25s} {item["attributes"]["endTime"][0:10]:10s} {item["attributes"]["state"]}')
                return f'{self.hostname} netbackup backup {item["attributes"]["state"]} on {item["attributes"]["endTime"][0:10]:10s}'
                break
        except:
            return f'{self.hostname} no backup'

        print("=========")
        print("*********")



class SiteScopeClient():

    SITESCOPR_PASSWORD = b'9\xd4\x92\x8b\xfe\x81q\xc9\xa4\xe3\xf0\xfcG\x1c\x9f\xd3\x19\xd5\x9bH\xfd\xb32\xe7\x81e\x14\xa2\xb7\xc7\x9f\x18\x98\n\xceRJup\x94\xcc\xc3D\xf2P\xce\xbcf\xe13<\xf14\r\x83\x12\x1b\x8bBHaU\xa1\xc5\xcc\xfe\xed\xa5\xb1\'\x86\x89\x98\x89P\xe6y`\xab\x83\xfb\xaa\x03C=\x1c\x90\x9e\x80\xbd!\x14\xcc\x9cO\x8fU\xb6M[.\xc5\x80\xf7?2\x1f,\xac\xd5G\xc5\x12\x7f\xfd\xea\x06\xbf\xcd\x94"I\x10r\xbd\x04\x8a\x94\xbde\x89[\x14\x9fN\xec-\xb6\xc0\\5\xa0J\xbc\xd3Jm<C\x0eX\xe3\xf6\xea\x93\xa8?H\x12\x9aX\xcbT\xdb-9\xb3\x88\x01\xfcr\xdd)\x1cT\xf5\xe6\x0f\xcec\x80\xde>\\\xde\x13\x0c\x86\xe0Q\xd8Z\x0c\xefH\x91\xd1\x9c\x00\xa1\xf5\x89=\xbaL.\xc7\xbc(v\x89\x17{-k\xa1:\xfb$Dhc\x15?F\x8cA\x95\xdc\x07\xee\xd8Y\x1bQ\xe6\x14A\xbb\x0e\x86+\xbdZ\xa3\xfe\xb6\x19\xd4\xd8\xd0\xa9z/\x8a5'

    TIME_DELTA = 1 		 # means delta is 1 day

    BLACKOUT_LENGTH = 1      # means blackout length = 1 hr

    def __init__(self, row):
        self.row = row

    def get_password(self):
        from cryptography.hazmat.primitives.asymmetric import rsa, padding
        from cryptography.hazmat.primitives import serialization, hashes


        with open('/root/.sitescope/priv.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        decrypted = private_key.decrypt(
            SiteScopeClient.SITESCOPR_PASSWORD,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        password = decrypted.decode()
        return password


    def cal_date(self, start_suppress):
        from_datetime = datetime.strptime(start_suppress, '%Y%m%d%H%M')
        from_diff = int(from_datetime.timestamp() - datetime.now().timestamp())
        return from_diff


    def check_monitor(self, host: str, group_name: str, web_URL: str):
        find_url = f'{web_URL}/api/monitors/group/properties'
        params = {'fullPathToGroup': group_name}
        response = requests.get(find_url, params=params, verify=False,
                                auth=HTTPBasicAuth(os.environ['SITESCOPE_USER'], SITESCOPE_PASSWORD))
        output = json.loads(response.text)
        print(f"{host} {output['status']}")


    def blackout(self):
        if self.row[0] == "#":
            global desc
            desc = self.row[1:]
            return

        blackout_duration = SiteScopeClient.BLACKOUT_LENGTH * 3300 * 1000

        mon_state = 'disable'
        host, hour_min = self.row.split(',')
        if not host:
            print("Error: no hostname provides.")
            sys.exit(1)

        import socket
        this_host = socket.gethostname()
        if this_host[0] == 'n' and host[0] == 'n':
            web_URL = 'https://n1vsmobmaw0010.nonprod.empf.local/SiteScope'
        elif this_host[0] == 'p' and host[0] == 'p':
            web_URL = 'https://p1vsmobmaw0010.prod.empf.local/SiteScope'
        else:
            return

        find_url = f'{web_URL}/api/monitors'
        set_url = f'{web_URL}/api/monitors/group/status'

        #if args.time:
        from datetime import date, datetime, timedelta
        today = datetime.now()
        tmr = today + timedelta(SiteScopeClient.TIME_DELTA)
        start_suppress = tmr.strftime("%Y%m%d") + hour_min[0:4]

        params = {
            'entity_type': '', # for both monitors and groups.
            'searchregex': 'true',
            'name': host
        }

        # Find the group name in sitescope
        response = requests.get(find_url, params=params, verify=False,
                                auth=HTTPBasicAuth('administrator', self.get_password()))
        if response.status_code != 200:
            print("Error: Auth failed.")
            sys.exit(1)
        groups_dict = json.loads(response.text)
        if not bool(groups_dict):
            print(f"{host} is NOT in sitescope.")
            return

        # Post to sitescope
        for k, group_name in enumerate(groups_dict):
            if groups_dict[group_name] == 'Group' and host in group_name:
                if mon_state == "check":
                    self.check_monitor(host, group_name, web_URL)
                    break
                # Suppress monitoring for 4 hours
                from_diff = self.cal_date(start_suppress) * 1000
                to_diff = from_diff + blackout_duration
                params = {
                    'fullPathToGroup': group_name,
                    'enable': mon_state,
                    'fromTime': str(from_diff),
                    'toTime': str(to_diff),
                    'description': f"SMAX{desc}"
                }
                response = requests.post(set_url, data=params, verify=False,
                                        auth=HTTPBasicAuth('administrator', self.get_password()))

                if host[2] == "p":
                    print(f"WARNING: You need to disable NNMI - {host}.")

                if response.status_code == 204:
                    return f"{response.status_code}  {host} blackout start from {start_suppress} for {blackout_duration/1000} secs."
                else:
                    return f"{response.status_code}  {host} blackout failed."
                break


def main():
    # Get server list from p2vsmsautl0010:/repo/sasa
    url='http://10.122.0.21:3001/sasa/servers.csv'
    res = requests.get(url, stream=True)
    with open('/tmp/servers.csv', "w") as f:
        f.write(res.text)

    import csv
    with open('/tmp/servers.csv', "r") as csv_f:
        for row in csv_f:
            if row[0] == "#":
                global desc
                desc = row[1:]
                continue
            else:
                sitescope_c =  SiteScopeClient(row)
                sitescope_output = sitescope_c.blackout()
                nbu_c = NBUClient(row)
                nbu_output = nbu_c.call_server()
            print(f"{sitescope_output} {nbu_output}")
    os.unlink('/tmp/servers.csv')


if __name__ == '__main__':
    main()
