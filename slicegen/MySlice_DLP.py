# Leave this statement impports the
# objects that represent FABRIC resources. 
from  fabric_objects import *

# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


slice = CfSlice(__name__, rocky_linux_workaround=False)

node1 = CfNode(slice, 'CMBS4Node1', image,
                disk=disk, cores=cores, ram=ram, site='TACC', storage="CMB-S4-phase-one")
net1 = CfL3Network(slice, 'net1', type='IPv4')


node2 = CfNode(slice, 'CMBS4Node2', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')
net2 = CfL3Network(slice, 'net2', type='IPv4')


CfNic(slice, "Node1.NIC1", node1, net1)
CfNic(slice, "Node2.NIC1", node2, net2)


#CFCmds(slice, "Standard Install", node1, "hostname")
#CFCmds(slice, "Standard Install", node2, "hostname")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
