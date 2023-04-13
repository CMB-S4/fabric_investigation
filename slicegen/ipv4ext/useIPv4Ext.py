
import os
import time

import datetime
from  datetime import timedelta

import json
import traceback

from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

try:
    fablib = fablib_manager()

    fablib.show_config();
except Exception as e:
    print(f"Exception: {e}")


from plugins import Plugins
try:
    print("Loading Plugins")
    Plugins.load()
except Exception as e:
    traceback.print_exc()

print("Done Loading Plugins")


slice_name = 'MySliceMar31A'
site1='NCSA'

node1_name = 'Node1'

network1_name='net1'

node1_nic_name = 'nic1'

image = 'default_rocky_8'
cores = 4
ram = 16
disk = 10


try:
    #Create Slice
    slice = fablib.new_slice(name=slice_name)

    # Node1
    node1 = slice.add_node(name=node1_name, site=site1)
    node1.set_capacities(cores=cores, ram=ram, disk=disk)
    node1.set_image(image)

    iface1 = node1.add_component(model='NIC_Basic', name=node1_nic_name).get_interfaces()[0]

    net1 = slice.add_l3network(name=network1_name, interfaces=[iface1], type='IPv4Ext')

    #Submit Slice Request
    slice.submit()
except Exception as e:
    print(f"Exception: {e}")



