#!/usr/bin/env python3

import os
import re
import subprocess


def find_rpm_version(name):
    o = os.system(f"rpm -q {name} > /dev/null")
    if o != 0:
        return None
    cmd = f'rpm -q {name} --queryformat '
    cmd += '"%{VERSION} %{RELEASE}\n"|sort -n | tail -1'
    output = subprocess.check_output(cmd, shell=True)
    version=output.decode("utf-8").rstrip()
    return version


def compare(rpm_version, rpm_release, ey_needs):
    # print(rpm_version, rpm_release, ey_needs)
    ey_want = ey_needs
    rpm_arr = rpm_version.split('.')
    rpm_release = re.sub('.el8.*', '', rpm_release)
    rpm_arr += rpm_release.split('.')
    try:
        for i in range(len(rpm_arr)):
            if int(rpm_arr[i]) > int(ey_want[i+1].strip() or 0):
            # if ey version is > os rpm version, return False
                return True, rpm_arr
            if int(rpm_arr[i]) == int(ey_want[i+1].strip() or 0):
                continue
            else:
                return "OS", False, rpm_arr
        # rpm verion === ey version
        return True, rpm_arr
    except Exception as e:
        print(f"Exception: {ey_want} {str(e)}")


if __name__ == "__main__":
    count = 0
    pattern = r'^([^\.]+(?:\-1\.8\.0\-openjdk.*)?)\-([a-z0-9]+)[\-\.](\d+)[\-\.]?(\d+)?[\.\-]?(\d+)?[\.\-](\d+)?[\.\-](\d+)?'
    pattern2 = r'^([a-z0-9\.\-]+)\-(.+)\-(\d+)'
    with open("ey.list") as myrpm:
        for row in myrpm:
            row = row.rstrip()
            # Get EY version
            ey_needs = re.findall(pattern, row)
            if len(ey_needs) == 0:
                # print(f"Error: {str(row)}")
                ey_needs = re.findall(pattern2, row)
                print(ey_needs)
            else:
                ey_needs = list(ey_needs[0])
                ey_needs = [x for x in ey_needs if x != '']
                # Get rpm version in OS
                os_version = find_rpm_version(ey_needs[0])
                if os_version:
                    rpm_version, rpm_release = os_version.split(" ")
                    print(f"{ey_needs[0]} ! {compare(rpm_version, rpm_release, ey_needs)} > EY {ey_needs}")
                else:
                    print(f"Warning: {ey_needs[0]} not found in OS.")
