import json
import random
from db.store import global_object, BackgroundTasks, bt, open_json
from web_ui.app_config import app, session
from db.models import Host, CPUThreshold, MEMThreshold

def get_hosts():
    # global store
    global bt
    if not bt:
        # Background thread maintains the global store
        bt = BackgroundTasks()
        bt.start()
    global global_object
    return global_object.store


def add_host(hostname, res_dict):
    try:
        cpu_t = CPUThreshold(cpu_threshold=res_dict["cpu_threshold"])
        mem_t = MEMThreshold(mem_threshold=res_dict["mem_threshold"])
        host = Host(hostname=hostname, cpu_threshold=[cpu_t], mem_threshold=[mem_t])
        session.add(host)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
