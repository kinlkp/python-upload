from api_libs.ovirt import oVirt

import sys


class oVirtStorage(oVirt):
    
    def __init__(self, name, action, acces_token):
        super().__init__(name, action, acces_token)
        self.obj_type = "storage"
        self.xml_tag = "storage_domain"
        self.vid = None
        
    
    def get_obj_url_request_body(self):
        url_base = f"{self.api_url}/storagedomains"
        maps = {
            "list": [f"{url_base}", ""],
            "get":[f"{url_base}/{self.vid}", ""],
            # "getTemplates":[f"{url_base}/{vid}/templates", ""],
            "getSnapshots":[f"{url_base}/{self.vid}/disksnapshots", ""],
            # "deleteSnapshots":[f"{url_base}/{vid}/disksnapshots", ""],
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
        return super().list(url)
        
        
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
            
            
class oVirtStorageSnapshot(oVirtStorage):
    
    def __init__(self, name, action, acces_token):
        super().__init__(name, action, acces_token)
        self.obj_type = "storage"
        self.xml_tag = "storage_domain"
        self.vids = []
        self.vid = None
                  
        
    def list(self):
        self.action = "getSnapshots"
        domains = super().list()
        for d in domains:
            self.vid = d.get('id')
            print(self.get_obj_url_request_body())
                      
            
        
        