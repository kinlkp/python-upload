
import json
import os
import requests
import os.path
import time
import sys


HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

PARAMS = {
    "grant_type": "password",
    "scope": "ovirt-app-api",
    "username": "admin@internal",
    "password": "password"
}

ROOT_CA = "ca.pem"

class Auth:
    
    file_path = f"/tmp/access_token_{os.environ.get('OLVM_FQDN')}.ovirt"
    oAuth_URL = f"https://{os.environ.get('OLVM_FQDN')}/ovirt-engine/sso/oauth/token"
    
    
    @staticmethod
    def authenticate():
        token = None
        if os.path.isfile(Auth.file_path):
            with open(Auth.file_path) as f:
                token = f.readline()
            token_json = json.loads(token)
            token = Auth._check_existing_token(token_json)
            
        if not token:
            oauth_output = requests.post(
                url=Auth.oAuth_URL,
                params=PARAMS,
                verify=ROOT_CA,
                headers=HEADERS,
            )
            if oauth_output.status_code != 200:
                print("Error: auth failed.")
                sys.exit()
            Auth._access_token_save(oauth_output.text)
            x = json.loads(oauth_output.text)
            token = x["access_token"]
            
        return token
    
    
    @staticmethod
    def _check_existing_token(token_json):

        json_expiry_time = int(token_json["exp"]) / 1000
        # Check if the access token is expired
        delta = json_expiry_time - int(time.time())
        if delta < 0:
            return None

        token = token_json["access_token"]
        # Test if the token is still valid
        oauth_output = requests.get(
            url=f"https://{os.environ.get('OLVM_FQDN')}/ovirt-engine/api",
            verify=ROOT_CA,
            headers={
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/xml',
                'Accept': 'application/xml'
            },
            timeout=2
        )
        if oauth_output.status_code != 200:
            return False
            
        return token
    
    
    @staticmethod
    def _access_token_save(token: str):
        with open(Auth.file_path, 'w') as f:
            f.write(token)
