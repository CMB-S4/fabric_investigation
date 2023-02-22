
import os
import time
import datetime
from  datetime import timedelta
import json
import traceback

from fabrictestbed_extensions.fablib.fablib import fablib

slice_name='MySliceFeb21A'

try:
    slice = fablib.get_slice(name=slice_name)
except Exception as e:
    print(f"Exception: {e}")

node1_name = 'CMBS4Node_fiu1'

try:
    print("Node1 " + node1_name) 
    storage_name = "CMB-S4-phase-one"
    node1 = slice.get_node(name=node1_name)
    storage = node1.get_storage(storage_name)
    print(f"Storage Device Name: {storage.get_device_name()}")

    stdout,stderr = node1.execute(f"sudo mkdir /mnt/fabric_storage; "
                                 f"sudo mount {storage.get_device_name()} /mnt/fabric_storage; "
                                 f"df -h")

except Exception as e:
    print(f"Exception: {e}")

