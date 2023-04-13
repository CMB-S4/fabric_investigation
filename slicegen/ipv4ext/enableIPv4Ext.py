
import datetime
import json
import os
import time
import traceback
from  datetime import timedelta

from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
from plugins import Plugins

try:
    fablib = fablib_manager()
    fablib.show_config();
except Exception as e:
    print(f"Exception: {e}")

try:
    print("Loading Plugins")
    Plugins.load()
except Exception as e:
    traceback.print_exc()
print("Done Loading Plugins")


slice_name = 'MySliceMar31A'

network1_name='net1'

try:
    # Get Existing Slice
    slice = fablib.get_slice(name=slice_name)

    network1 = slice.get_network(name=network1_name)
    network1_available_ips = network1.get_available_ips()

    # Enable Public IPv4
    # Due to limited IPv4 address space, we use a single subnet for all the slices for a specific site
    # Please note the first IP on the subnet is requested to be made public. If the IP is already in use, ControlFramework assigns an available IP
    # and saves in the Labels. If no available IP is found, an error is returned.

    print("before change_public_ip ipv4")
    network1.change_public_ip(ipv4=[str(network1_available_ips[0])])
    print("after change_public_ip ipv4")

    # Uncomment to Disable Public IPv4
    # network1.update_labels(ipv4_subnet=[])
    # Submit an Existing Slice again => Modify !
    slice.submit()

except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()


