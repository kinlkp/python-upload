from api_libs.ovirt import oVirt
from datetime import datetime

import sys


class oVirtVM(oVirt):
    
    def __init__(self, name, action, acces_token):
        super().__init__(name, action, acces_token)
        self.obj_type = "vm"
        self.xml_tag = "vm"
        self.vid = None
        
    
    def get_obj_url_request_body(self):
        url_base = f"{self.api_url}/vms"
        # maps = {"key": ["url", "request_body"]}
        maps = {
            "shutdown": [f"{url_base}/{self.vid}/shutdown", f"{self.xml_header}<action/>"],
            "start": [f"{url_base}/{self.vid}/start", f"{self.xml_header}<action/>"],
            "list": [f"{url_base}", ""],
            "snapshot": [f"{url_base}/{self.vid}/snapshots", f"{self.xml_header}<snapshot><description>snapshot at {str(datetime.now())}</description></snapshot>"],
            "poweroff": [f"{url_base}/{self.vid}/stop", f"{self.xml_header}<action><force>true</force></action>"],
            "suspend": [f"{url_base}/{self.vid}/suspend", f"{self.xml_header}<action/>"],
            "delete": [f"{url_base}/{self.vid}", ""],
            "get":[f"{url_base}/{self.vid}", ""],
        }
        
        if not self.vid:
            return maps["list"]
        
        try:
            return maps[self.action]
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)
            sys.exit()
            
            
    def list(self):
        (url, _) = self.get_obj_url_request_body()
        super().list(url)
        
        
    def get(self):
        (url, _) = self.get_obj_url_request_body()
        self.vid = self.find(url)
        (url, _) = self.get_obj_url_request_body()
        xml_result = self.get_api(url)
        print(xml_result.text)

    
    def exec_task(self):
        if self.action == "list":
            self.list()
        elif self.action == "get":
            self.get()
        else:
            (url, _) = self.get_obj_url_request_body()
            self.vid = self.find(url)
            (url, request_body) = self.get_obj_url_request_body()
            super().exec_task(url, request_body)
