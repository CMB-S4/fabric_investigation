# Leave this statement impports the
# objects that represent FABRIC resources. 
from  fabric_objects import *


# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


slice = Slice('MySlice_DLP')

node1 = Node(slice, 'CMBS4Node_ncsa1', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')
net1 = L3Network(slice, 'net1')

Nic(slice, "Node1.NIC1", node1, net1)


#fo.Cmds(slice, "Standard Install", node1, "hostname")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
