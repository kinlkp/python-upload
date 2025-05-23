#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The script is used to create cyberark accounts in .xlsx
"""

DEFAULT_ACC = """p1psmwind0001,prsyadirad0001,CAT B System Team,Netbackup Server
p1psmwind0002,prsyadirad0001,CAT B System Team,Netbackup Server
p2psmwind0001,prsyadirad0001,CAT B System Team,Netbackup Server
p2psmwind0002,prsyadirad0001,CAT B System Team,Netbackup Server
p1vsmobmaw0010,prsydomaad0001,CAT B System Team,SiteScope Server
p1vsmsautw0001,prsydomaad0001,CAT B System Team,SA Console
p1vsmsautw0002,prsydomaad0001,CAT B System Team,SA Console
p1vsemepoc001,prsemepoad0001,CAT B System Team,MacAfee Server
p1vsmvcsaa0001,administrator@prod.empf.local,CAT B System Team,Vcenter
p1vsesmgt0001,prsemepoad0001,CAT B Security Team,Splunk Server
p1vsmcmpxw0002,prsydomaad0001,CAT B Development Team,UD server
p1vsmcmpxw0003,prsydomaad0001,CAT B Development Team,UD server
p1vsmsautl0010,root,CAT B System Team,saut server
p2vsmsautl0010,root,CAT B System Team,saut server
n1psmwind0001,npsyadirad0001,CAT B System Team,Netbackup Server
n1psmwind0002,npsyadirad0001,CAT B System Team,Netbackup Server
n2psmwind0001,npsyadirad0001,CAT B System Team,Netbackup Server
n2psmwind0002,npsyadirad0001,CAT B System Team,Netbackup Server
n1vsmobmaw0010,npsydomaad0001,CAT B System Team,SiteScope Server
n1vsemepoc001,npsemepoad0001,CAT B System Team,MacAfee Server
n1vsmvcsaa0001,administrator@nonprod.empf.local,CAT B System Team,vCenter
n1vsesmgt0001,npsemepoad0001,CAT B Security Team,Splunk Server
n1vsmcmpxw0002,npsydomaad0001,CAT B Development Team,UD Server
n1vsmcmpxw0003,npsydomaad0001,CAT B Development Team,UD Server"""

def get_account_name(hostname):
    account_name = ""
    if hostname[0] == "n":
        account_name += "np"
    elif hostname[0] == "p":
        account_name += "pr"
    elif hostname[0] == "o":
        account_name += "pr"

    outputs = ""
    ad = "ad0001"
    app = hostname[5:9]
    if hostname[3:5] == "a2" or hostname[3:5] == "db":
        # Print Cat A accounts
        ca = account_name + "ca" + app + ad
        outputs = f"{hostname},{ca},Cat A,{app} server\n"
        ce = account_name + "ce" + app + ad
        outputs += f"{hostname},{ce},Cat A,{app} server\n"
        # Print security team accounts
    elif hostname[3:5] == "se":
        se = account_name + "se" + app + ad
        outputs += f"{hostname},{se},Cat B Security team,{app} server\n"
    elif hostname[3:5] == "ne":
        se = account_name + "se" + app + ad
        outputs += f"{hostname},{se},Cat B Security team,{app} server\n"
    
    # Print system team accounts
    sy = account_name + "sy" + app + ad
    outputs += f"{hostname},{sy},Cat B System team,{app} server\n"
    
    # Print system team accounts
    if hostname[9] == "w":
        outputs += f"{hostname},{account_name}sylocaad0002,Cat B System team,{app} server\n"
        outputs += f"{hostname},{account_name}sydomaad0001,Cat B System team,{app} server\n"
        outputs += f"{hostname},{account_name}sycaadad0001,Cat B System team,{app} server\n"
    elif hostname[9] == "l":
        outputs += f"{hostname},root,Cat B System team,{app} server\n"

    if hostname[2] == "p":
        outputs += f"{hostname}-ilo,administrator,Cat B System team,{hostname} ilo\n"
        outputs += f"{hostname}-idrac,administrator,Cat B System team,{hostname} idrac\n"
        outputs += f"{hostname},root,Cat B System team,{hostname} root\n"

    return outputs

def main():
    print("hostname,account,team,description")
    print(DEFAULT_ACC)
    output = ""
    with open("servers.list") as f:
        while True:
            content = f.readline()
            if not bool(content):
                break
            output += get_account_name(content.rstrip().lower())

    print(output)

if __name__ == "__main__":
    main()
