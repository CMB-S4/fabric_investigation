
import os
import time

import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network

slice_name="TestSliceNov23A"

try:
    slice = fablib.get_slice(slice_name)

    node_name = 'CMBS4Node_fiu'
    node1_name = 'CMBS4Node_tacc1'
    node2_name = 'CMBS4Node_dall2'

    node = slice.get_node(name=node_name)        
    node1 = slice.get_node(name=node1_name)        
    node2 = slice.get_node(name=node2_name)        

    stdout, stderr = node.execute(f'ip addr show')
    print (stdout)
    print ("========================================")
    stdout, stderr = node1.execute(f'ip addr show')
    print (stdout)
    print ("========================================")
    stdout, stderr = node2.execute(f'ip addr show')
    print (stdout)
    print ("========================================")

except Exception as e:
    print(f"Fail: {e}")

