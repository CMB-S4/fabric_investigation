# Leave this statement impports the
# objects that represent FABRIC resources. 
from  fabric_objects import *

# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


slice = CfSlice(__name__)

node1 = CfNode(slice, 'CMBS4Node_ncsa1', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')
node2 = CfNode(slice, 'CMBS4Node_ncsa2', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')

net1 = CfL3Network(slice, 'net1')

CfNic(slice, "Node1.NIC1", node1, net1)
CfNic(slice, "Node2.NIC1", node2, net1)


CFCmds(slice, "Standard Install", node1, "hostname")
CFCmds(slice, "Standard Install", node2, "hostname")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
