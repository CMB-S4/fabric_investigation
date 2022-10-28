# Leave this statement impports the
# objects that represent FABRIC resources. 
from  fabric_objects import *
import os

# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


#
# sttop to test that all nodes can talk to each other
#
slice = CfSlice(os.path.basename(__name__))

ncsa1 = CfNode(slice, 'ncsa1', image, site='NCSA', cores=2)
ncsa2 = CfNode(slice, 'ncsa2', image, site='NCSA', cores=2)
ncsa_net = CfL3Network(slice, 'ncsa_net', type="IPv6")
CfNic(slice, "ncsa1.NIC" , ncsa1, ncsa_net)
CfNic(slice, "ncsa2.NIC" , ncsa2, ncsa_net)


tacc1 = CfNode(slice, 'tacc1', image, site='TACC', cores=2)
tacc2 = CfNode(slice, 'tacc2', image, site='TACC', cores=2)
tacc_net = CfL3Network(slice, 'tacc_net', type="IPv6")
CfNic(slice, "tacc1.NIC" , tacc1, tacc_net)
CfNic(slice, "tacc2.NIC" , tacc2, tacc_net)

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
