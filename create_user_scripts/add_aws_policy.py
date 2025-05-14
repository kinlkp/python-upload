#!/usr/bin/env python

# The script adds the EKS describe policy to IAM user
# so that the user can get kubeconfig


import boto3
import json
from utils import get_args


POLICY_NAME = 'CtrlIAMUserDescribeEKS'
POLICY_JSON = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:DescribeCluster",
                "eks:ListClusters"
            ],
            "Resource": "*"
        }
    ]
}


def create_policy(iam):
    # Create a policy
    response = iam.create_policy(
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(POLICY_JSON)
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to create.")
    print(f"Policy {POLICY_NAME} is added.")
    return response['Policy']['Arn']


def attach_policy_to_user(iam, username):
    response = iam.get_user(UserName = username)
    
    response = iam.attach_user_policy(
        UserName=username,
        PolicyArn=find_policy_arn(iam)
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Policy {POLICY_NAME} is attached to {username}")
        return True
    return False


def find_policy_arn(iam):
    found = False
    arn = ''
    res = iam.list_policies(Scope='Local')
    responses = res['Policies']
    for response in responses:
        if response['PolicyName'] == POLICY_NAME:
            found = True
            arn = response['Arn']
                        
    if not found:
        arn = create_policy(iam)

    return arn


def main():
    args = get_args()
    username = args.username

    # Create IAM client
    iam = boto3.client('iam')
    if not attach_policy_to_user(iam, username):
        print(f"Error: Policy {POLICY_NAME} cannot attach to {username}")


if __name__ == '__main__':
    main()