
import os
import time

# import datetime
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

node1_name = 'Node1'
network1_name='net1'

try:
    #Create Slice
    slice = fablib.get_slice(name=slice_name)

    # Get Node
    node1 = slice.get_node(name=node1_name)
    # Get Network
    network1 = slice.get_network(name=network1_name)
    # Get Interface
    node1_iface = node1.get_interface(network_name=network1_name)

    # Get Assigned Public IP returned by Control Framework
    node1_addr = network1.get_fim_network_service().labels.ipv4[0]
    print("node1_addr")
    print(node1_addr)

    # Configure the assigned public IP
    # (shorter?) node1_addr = network1_available_ips.pop(0)
    node1_iface.ip_addr_add(addr=node1_addr, subnet=network1.get_subnet())

    node1.execute(f'sudo ip route add {network1.get_gateway()} dev ens7');
    node1.execute(f'sudo ip route add 141.142.0.0/16 via {network1.get_gateway()}')
    node1.execute(f'sudo ip route add 128.55.0.0/16 via {network1.get_gateway()}')
    node1.execute(f'sudo ip route add 72.36.0.0/16 via {network1.get_gateway()}')

    print("===========================================================================")
    stdout, stderr = node1.execute(f'ip addr show {node1_iface.get_os_interface()}')
    print("===========================================================================")
    stdout, stderr = node1.execute(f'ip route list')
    print("===========================================================================")

except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()


