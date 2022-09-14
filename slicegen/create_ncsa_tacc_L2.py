
import os
import time
import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib

slice_name = 'MySliceSep12B'
site = 'NCSA'
site2 = 'TACC'
node_name = 'CMBS4Node_ncsa1'
node2_name = 'CMBS4Node_tacc2'
image = 'default_rocky_8'

cores = 32
ram = 128
disk = 100

network_name='net1' 
node_nic_name = 'nic1'
node2_nic_name = 'nic2'

try:
    #Create Slice
    slice = fablib.new_slice(name=slice_name)

    # Node1
    node1 = slice.add_node(name=node_name, site=site)
    node1.set_capacities(cores=cores, ram=ram, disk=disk)
    node1.set_image(image)
    iface1 = node1.add_component(model='NIC_Basic', name=node_nic_name).get_interfaces()[0]

    # Node2
    node2 = slice.add_node(name=node2_name, site=site2)
    node2.set_capacities(cores=cores, ram=ram, disk=disk)
    node2.set_image(image)
    iface2 = node2.add_component(model='NIC_Basic', name=node2_nic_name).get_interfaces()[0]

    # Network
    net1 = slice.add_l2network(name=network_name, interfaces=[iface1, iface2])

    
    print("About to submit ...")
    time.sleep(4)
    #Submit Slice Request
    slice.submit()
    print("Submitted")
    # slice.submit(wait_progress=True)
except Exception as e:
    print(f"Exception: {e}")

