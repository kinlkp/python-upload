# Manage virtual machine in ovirt platform by REST api 

## List all VMs
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "*" --action list

Result

    (venv) [root@ctrl ovirt-api_py]# python3 main.py --vm_name '*' --action list
    HostedEngine                                       1b26b3a0-de88-499b-a1e9-435ce1d8bbd8
    rhel9_clone_in_vcenter_20240326160017              777e0fff-3964-46f6-aede-b272bafbe95d
    VinChin_ol89                                       4740bc50-3803-46e6-ba8c-8a78b8d17ea1
    VinChin_ubuntu_testing                             b4b384a2-7a1c-406a-b170-497de25263ed
    VinChin_Veeam_Backup_Server                        ef2f25b0-8e63-4025-a21f-5b0fb166be68
    VinChin_Veeam_Backup_Server_20240320163308         fe2d6940-2f08-4cfa-8371-6fd03231e47f
    win2016xxaxads                                     0cb6cb6c-dda7-4c41-8658-e6acb1caae0d
    win2019                                            521cbcc1-49a5-4629-a4f8-808da7de4592


## Start VM
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "ol7a" --action start

## Shutdown VM
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "ol7a" --action stop

## Snapshot VM
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "ol7a" --action snapshot

## Delete VM
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "ol7a" --action delete

## Print debug
    export OLVM_FQDN="manager2.oc.example"
    python3 main.py --vm_name "ol7a" --action start --debug 1

## API Reference

https://www.ovirt.org/documentation/doc-REST_API_Guide/
