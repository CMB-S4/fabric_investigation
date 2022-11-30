
import os
import time
import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib

slice_name = 'TestSliceNov23A'
site = 'FIU'
site1 = 'TACC'
site2 = 'DALL'
node_name = 'CMBS4Node_fiu'
node1_name = 'CMBS4Node_tacc1'
node2_name = 'CMBS4Node_dall2'
image = 'default_rocky_8'
cores = 16
ram = 64
disk = 100

network_name_1t='net1t' 
network_name_2t='net2t' 
network_name_12='net12' 
nodet_a_nic_name = 'nict_a'
nodet_b_nic_name = 'nict_b'
node1_a_nic_name = 'nic1_a'
node1_c_nic_name = 'nic1_c'
node2_b_nic_name = 'nic2_b'
node2_c_nic_name = 'nic2_c'
print("Set Parameters")

try:
    #Create Slice
    slice = fablib.new_slice(name=slice_name)

    # Gateway Node
    nodet = slice.add_node(name=node_name, site=site)
    nodet.set_capacities(cores=cores, ram=ram, disk=disk)
    nodet.set_image(image)
    ifacet_a = nodet.add_component(model='NIC_Basic', name=nodet_a_nic_name).get_interfaces()[0]
    ifacet_b = nodet.add_component(model='NIC_Basic', name=nodet_b_nic_name).get_interfaces()[0]

    # Node1
    node1 = slice.add_node(name=node1_name, site=site1)
    node1.set_capacities(cores=cores, ram=ram, disk=disk)
    node1.set_image(image)
    iface1_a = node1.add_component(model='NIC_Basic', name=node1_a_nic_name).get_interfaces()[0]
    iface1_c = node1.add_component(model='NIC_Basic', name=node1_c_nic_name).get_interfaces()[0]

    # Node2
    node2 = slice.add_node(name=node2_name, site=site2)
    node2.set_capacities(cores=cores, ram=ram, disk=disk)
    node2.set_image(image)
    iface2_b = node2.add_component(model='NIC_Basic', name=node2_b_nic_name).get_interfaces()[0]
    iface2_c = node2.add_component(model='NIC_Basic', name=node2_c_nic_name).get_interfaces()[0]

    # Networks
    net1t = slice.add_l2network(name=network_name_1t, interfaces=[ifacet_a, iface1_a])
    net2t = slice.add_l2network(name=network_name_2t, interfaces=[ifacet_b, iface2_b])
    net12 = slice.add_l2network(name=network_name_12, interfaces=[iface1_c, iface2_c])

    
    print("About to submit ...")
    #Submit Slice Request
    slice.submit()
    print("Submitted")
    # slice.submit(wait_progress=True)
except Exception as e:
    print(f"Exception: {e}")

