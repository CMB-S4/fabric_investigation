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
# Simple setup to gebug why nodes don't work
# at least on DOn's mac
#
slice = CfSlice(os.path.basename(__file__)[:-3])

node1 = CfNode(slice, 'CMBS4Node_ncsa1', image,
                disk=disk, cores=cores, ram=ram,
               site='NCSA')
CfCmds(slice, "example command", node1, "hostname")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
