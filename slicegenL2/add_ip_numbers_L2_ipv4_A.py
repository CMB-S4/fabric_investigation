
import os
import time

import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network

slice_name="TestSliceNov23A"

try:
    slice = fablib.get_slice(slice_name)

    network_name='net1t'
    subnet = IPv4Network("198.187.27.0/24")

    available_ips = subnet.hosts()

    node1_name = 'CMBS4Node_fiu'
    node2_name = 'CMBS4Node_tacc1'

    node1 = slice.get_node(name=node1_name)        
    node1_iface = node1.get_interface(network_name=network_name) 
    node1_addr = next(available_ips)
    print("Node 1 info")
    print(node1)
    print(node1_addr)
    node1_iface.ip_addr_add(addr=node1_addr, subnet=subnet)


    node2 = slice.get_node(name=node2_name)        
    node2_iface = node2.get_interface(network_name=network_name)  
    node2_addr = next(available_ips)
    print("Node 2 info")
    print(node2)
    print(node2_addr)
    node2_iface.ip_addr_add(addr=node2_addr, subnet=subnet)

    print("Interfaces")
    print(node1_iface)
    print(node2_iface)

    print(node1_iface.get_os_interface())
    print(node2_iface.get_os_interface())

    stdout, stderr = node1.execute(f'ip addr show {node1_iface.get_os_interface()}')
    print (stdout)
    stdout, stderr = node2.execute(f'ip addr show {node2_iface.get_os_interface()}')
    print (stdout)

except Exception as e:
    print(f"Fail: {e}")

