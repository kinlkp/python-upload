#!/usr/bin/python3

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
            try:
                if int(rpm_arr[i]) > int(ey_want[i+1].strip() or 0):
                    # if ey version is > os rpm version, return False
                    return "OS", True, rpm_arr
                if int(rpm_arr[i]) == int(ey_want[i+1].strip() or 0):
                    # rpm verion === ey version, go to check next value 
                    continue
                else:
                    # if os version is < os rpm version, return False
                    return "OS", False, rpm_arr
            except ValueError:
                if rpm_arr[i] > ey_want[i+1].strip():
                    return "OS", True, rpm_arr
                if rpm_arr[i] == ey_want[i+1].strip():
                    continue
                else:
                    return "OS", False, rpm_arr
        return "OS", True, rpm_arr
    except:
        print(f"{ey_want} exception")


if __name__ == "__main__":
    count = 0
    with open("ey.list") as myrpm:
        for row in myrpm:
            pattern = r'^([^\.]+(?:\-1\.8\.0\-openjdk.*)?)\-([a-z0-9]+)[\-\.](\d+)[\-\.]?(\d+)?[\.\-]?(\d+)?[\.\-](\d+)?[\.\-](\d+)?'
            pattern2 = r'^([a-z0-9\.\-]+)\-(.+)\-(\d+)'
            row = row.rstrip()
            # Get EY version
            if "openssl" in row:
                pattern = r'^(openssl[\-a-z]*)-(\d+).(\d+).([a-z0-9]+)-(\d+).el8[_0-9]*'
            if "cockpit-podman" in row:
                pattern = r'^(cockpit-podman)-(\d+)\.?(\d+)?-(\d+).modul'
            if "less" in row:
                pattern = r'^(less)-(\d+)\.?(\d+)?-(\d+).el8'
            if "jose" in row:
                pattern = r'^(jose)-(\d+)\.?(\d+)?-(\d+).el8'
            if "python3.11" in row:
                pattern = r'(^python3.11)-(\d+).(\d+).(\d+)'
            ey_needs = re.findall(pattern, row)
            if len(ey_needs) == 0:
                # print(f"Error: {str(row)}")
                ey_needs = re.findall(pattern2, row)
                print(f"{ey_needs} cannot match")
            else:
                ey_needs = list(ey_needs[0])
                ey_needs = [x for x in ey_needs if x != '']
                print(ey_needs[1])
                continue
                # Get rpm version in OS
                os_version = find_rpm_version(ey_needs[0])
                if os_version:
                    rpm_version, rpm_release = os_version.split(" ")
                    print(f"{ey_needs[0]} ! {compare(rpm_version, rpm_release, ey_needs)} > EY {ey_needs}")
                else:
                    print(f"Warning: {ey_needs[0]} not found in OS.")
