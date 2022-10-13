# Leave this statement impports the
# objects that represent FABRIC resources. 
from  fabric_objects import *

# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


slice = CfSlice(__name__)

observatory_node         = CfNode(slice, 'Observatory', image,
                             disk=disk, cores=cores, ram=ram, site='TACC')
map_maker_node           = CfNode(slice, 'MapMaker', image,
                             disk=disk, cores=cores, ram=ram, site='NCSA')
timestream_archive_node  = CfNode(slice, 'TimeArchive', image,
                             disk=disk, cores=cores, ram=ram, site='NCSA')
transients_node          = CfNode(slice, 'Transients', image,
		             disk=disk, cores=cores, ram=ram, site='NCSA')
transient_archive_node   = CfNode(slice, 'TansArchive', image,
		             disk=disk, cores=cores, ram=ram, site='NCSA')

observatory_net = CfL3Network(slice, 'observatory_net')
compute_net     = CfL3Network(slice, 'compute_net')   
archive_net     = CfL3Network(slice, 'compute_net')

CfNic(slice, "Observatory.NIC1" , observatory_node,            observatory_net)
CfNic(slice, "MapMaker.NIC1"    , map_maker_node,              compute_net)
CfNic(slice, "TimeArchive.NIC1" , timestream_archive_node,     archive_net)
CfNic(slice, "Transients.NIC1"  , transients_node,             compute_net)
CfNic(slice, "TransArchive.NIC1", transient_archive_node, archive_net)



#CFCmds(slice, "Standard Install", node1, "hostname")
#CFCmds(slice, "Standard Install", node2, "hostname")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
