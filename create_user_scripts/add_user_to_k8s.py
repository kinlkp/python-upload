#!/usr/bin/env python

# Source: https://github.com/kubernetes-client
# The script adds user into EKS the configMap aws-auth and RoleBinding
# so that the user can run kubectl

from kubernetes import config, dynamic
from kubernetes.client import api_client
from kubernetes.dynamic.resource import ResourceField
from utils import get_args

import boto3


# Get AWS account id
def get_account_id():
    client = boto3.client("sts")
    return client.get_caller_identity()["Account"]


# Update K8s configMap aws-auth
def update_cm_awsauth(client, username):
    aws_account_id = get_account_id()
    configmap_name = "aws-auth"
    new_user = f"- userarn: arn:aws:iam::{aws_account_id}:user/{username}\n  username: {username}"
    
    api = client.resources.get(api_version="v1", kind="ConfigMap")
    # Get the configMap aws-auth
    configmap_result = api.get(name=configmap_name, namespace="kube-system")
    # Extract the attribute mapUsers
    users = configmap_result['data'].__getattr__("mapUsers")
    if not users:
        configmap_result['data'].__setattr__("mapUsers", new_user)
    else:
        # Add the new user to the end of string
        users = f"{users}\n{new_user}"
        configmap_result['data'].__setattr__("mapUsers", users)
        
    # Patch the configMap aws-auth
    configmap_patched = api.patch(name=configmap_name, namespace="kube-system", body=configmap_result)
    print(f"Username {username} is added into configMap aws-auth")

    
# Update K8s ClusterRoleBinding
def update_cluserrolebinding(client, username):
    clusterrolebinding_name = "developer"
        
    api = client.resources.get(api_version="v1", kind="ClusterRoleBinding")
    # Get the ClusterRoleBinding
    cluserrolebinding_result = api.get(name=clusterrolebinding_name, namespace="")
    # Define the resource for the new user
    resourcefield = ResourceField({'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'User', 'name': f'{username}'})
    cluserrolebinding_result.subjects.append(resourcefield)

    # Patch the ClusterRoleBinding
    configmap_patched = api.patch(
        name=clusterrolebinding_name, namespace="", body=cluserrolebinding_result
    )
    print(f"Username {username} is added into ClusterRoleBinding {clusterrolebinding_name}")

    
# Update K8s RoleBinding
def update_rolebinding(client, username):
    rolebinding_name = "developer"
    
    api = client.resources.get(api_version="v1", kind="RoleBinding")
    # Get the RoleBinding
    rolebinding_name_result = api.get(name=rolebinding_name, namespace="ctrl-apps")
    # Define the resource for the new user
    resourcefield = ResourceField({'apiGroup': 'rbac.authorization.k8s.io', 'kind': 'User', 'name': f'{username}'})
    rolebinding_name_result.subjects.append(resourcefield)
    
    # Patch the RoleBinding
    configmap_patched = api.patch(
        name=rolebinding_name, namespace="", body=rolebinding_name_result
    )
    print(f"Username {username} is added into RoleBinding {rolebinding_name}")


def main():
    args = get_args()
    username = args.username
    
    # Creating a dynamic client
    client = dynamic.DynamicClient(
        api_client.ApiClient(configuration=config.load_kube_config())
    )
    update_cm_awsauth(client, username)
    update_cluserrolebinding(client, username)
    update_rolebinding(client, username)
    

if __name__ == "__main__":
    main()
