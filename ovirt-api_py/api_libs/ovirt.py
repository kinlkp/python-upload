
import xml.etree.ElementTree as ET
import requests
import os
import sys

ROOT_CA = "ca.pem"
   

class oVirt:
    
    timeout = 5
    xml_header = "<?xml version='1.0' encoding='utf-8'?>"
    api_url = f"https://{os.environ.get('OLVM_FQDN')}/ovirt-engine/api"
    
    def __init__(self, name, action, acces_token):
        self.name = name
        self.action = action
        self.obj_type = None
        self.xml_tag = None
        self.auth_headers = {
            'Authorization': f"Bearer {acces_token}",
            'Content-Type': 'application/xml',
            'Accept': 'application/xml'
        }
        
        
    def exec_task(self, url, request_body=None):
        
        if self.action == "delete":
            action_result = self.delete_api(url, request_body)
            print(f"http status code: {action_result.status_code}")
        else:
            action_result = self.post_api(url, request_body)
            print(f"http status code: {action_result.status_code}")            

            
    def list(self, url):
        xml_string = self.get_api(url)
        root = ET.ElementTree(ET.fromstring(xml_string.text))
        all_xml = root.findall(self.xml_tag)
        for xml in all_xml:
            if self.action == "list":
                print("%-50s %-50s" % (xml.find('name').text, xml.get('id')))
        return all_xml
            
        
    def find(self, url):
        vid = None
        xml_string = self.get_api(url)
        root = ET.ElementTree(ET.fromstring(xml_string.text))
        for xml in root.findall(self.xml_tag):
            if xml.find('name').text == self.name:
                return xml.get('id')
            
                
    def get_api(self, url: str):
        ovirt_url = url
        try:
            private_url_response_xml = requests.get(
                timeout=self.timeout,
                url=ovirt_url,
                verify=ROOT_CA,
                headers=self.auth_headers,
                params={
                    "search": f"name={self.name}", # url encode is done by python library
                    "case_sensitive": "false"
                    }
                )
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)
            sys.exit()

        return private_url_response_xml
    
    
    def post_api(self, url: str, request_body: str):
        ovirt_url = url
        try:
            private_url_response_xml = requests.post(
                timeout=self.timeout,
                url=ovirt_url,
                verify=ROOT_CA,
                headers=self.auth_headers,
                data=request_body
                )
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)
            sys.exit()

        # Print xml
        return private_url_response_xml
    
    
    def delete_api(self, url: str, request_body: str):
        ovirt_url = url
        try:
            private_url_response_xml = requests.delete(
                timeout=self.timeout,
                url=ovirt_url,
                verify=ROOT_CA,
                headers=self.auth_headers,
                )
            print(private_url_response_xml.text)
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)
            sys.exit()
        # Print xml
        return private_url_response_xml
    
