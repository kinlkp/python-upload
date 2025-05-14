#!/bin/python3

import re
import subprocess


def find_rpm(name):
	cmd = f"rpm -qi {name} | grep Version"
	cmd += "| awk -F':' '{print $2}' | sed -e 's/^ //' "
	output = subprocess.check_output(cmd, shell=True)
	version=output.decode("utf-8").rstrip()
	print(version)


if __name__ == "__main__":
	count = 0
	pattern = r'^([^\.]+)\-([a-z0-9]+)[\-\.](\d+)[\-\.]?(\d+)?[\.\-]?(\d+)?'
	with open("/var/tmp/ey.list") as myrpm:
			for row in myrpm:
					row = row.rstrip()
					matches = re.findall(pattern, row)
					if len(matches) == 0:
							print(f"Error: {str(row)}")
					else:
							find_rpm(matches[0][0])

