
import os
import time
import json
import traceback

from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

fablib = fablib_manager()

slice_name = 'MySliceFeb21A'

# site = <SITE_THAT_CONAINS_YOUR_VOLUME>
# storage_name = <NAME_OF_YOUR_VOLUME>
site1 = "FIU"
storage_name = "CMB-S4-phase-one" 

node1_name = 'CMBS4Node_fiu1'
image = 'default_rocky_8'
cores = 4
ram = 16
disk = 100

try:
    #Create Slice
    slice = fablib.new_slice(name=slice_name)

    node1 = slice.add_node(name=node1_name, site=site1)
    node1.set_capacities(cores=cores, ram=ram, disk=disk)
    node1.add_storage(name=storage_name)

    print("About to submit ...")
    slice.submit()
except Exception as e:
    print(f"Exception: {e}")

