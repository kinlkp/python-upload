import random
import threading
import time
import json
import os

# Store the host's metrics
class GObject:
    store = []
    
global_object = GObject()

# Background task
bt = None

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            global global_object
            # Clear the global list
            global_object.store.clear()
            global_object.store = open_json()
            time.sleep(2)


def open_json():
    with open(os.path.dirname(__file__) + "/db.json") as f:
        data = json.load(f)
        
    return data
