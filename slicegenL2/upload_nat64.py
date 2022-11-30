
import os
import time

import json
import traceback
from fabrictestbed_extensions.fablib.fablib import fablib

from ipaddress import ip_address, IPv6Address

slice_name="TestSliceNov23A"

try:
    slice = fablib.get_slice(slice_name)
    for node in slice.get_nodes():

        #If the node is an IPv6 Node then configure NAT64
        if type(ip_address(node.get_management_ip())) is IPv6Address:
            print(node.get_name()) 
            node.upload_file('nat64.sh','nat64.sh')

            stdout, stderr = node.execute(f'chmod +x nat64.sh && sudo ./nat64.sh')
            print(stdout)
            print(stderr)

        #Access non-IPv6 Services
        stdout, stderr = node.execute(f'sudo yum install -y -q git && git clone https://github.com/fabric-testbed/jupyter-examples.git')
        print(stdout)
        print(stderr)

        stdout, stderr = node.execute(f'ls jupyter-examples')
        print(stdout)
        print(stderr)


except Exception as e:
    print(f"Exception: {e}")

