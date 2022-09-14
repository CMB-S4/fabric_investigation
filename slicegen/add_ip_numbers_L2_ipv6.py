

import os
import time

import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network

slice_name="MySliceSep12B"
try:
    slice = fablib.get_slice(slice_name)
    print(slice_name)

#   subnet = IPv6Network("1234:5679::/64")
    subnet = IPv6Network("1232:5679::/64")

    available_ips = subnet.hosts()
    print("available_ips")
    print(available_ips)

    node1_name = 'CMBS4Node_ncsa1'
    node2_name = 'CMBS4Node_tacc2'

    network_name='net1'

    node1 = slice.get_node(name=node1_name)        
    node1_iface = node1.get_interface(network_name=network_name) 
    node1_addr = next(available_ips)
    print("Node 1 info")
    print(node1)
    print(node1_addr)
#   node1_iface.ip_addr_add(addr=node1_addr, subnet=subnet)
#   print("Before set_ip")
#   node1_iface.set_ip(ip=node1_addr, mtu=9000)
#   print("After set_ip")


    node2 = slice.get_node(name=node2_name)        
    node2_iface = node2.get_interface(network_name=network_name)  
    node2_addr = next(available_ips)
    print("Node 2 info")
    print(node2)
    print(node2_addr)
#   node2_iface.ip_addr_add(addr=node2_addr, subnet=subnet)
#   print("Before set_ip")
#   node2_iface.set_ip(ip=node2_addr, mtu=9000)
#   print("After set_ip")


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



