# Leave this statement impports the
# objects that represent FABRIC resources. 
import fabric_objects as fo


# default quantities for our nodes.
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100


slice = fo.Slice('MySliceSep12B')

net1 = fo.L2Network(slice, 'net1')
node1 = fo.Node(slice, 'CMBS4Node_ncsa1', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')
fo.Nic(slice, "Node1.NIC1", node1, net1)
node2 = fo.Node(slice, 'CMBS4Node_tacc2', image,
                            site="TACC")
fo.Nic(slice, "Node2.NIC1", node2, net1)

fo.Cmds(slice, "Standard Install", node1, "all dogs go to heaven")

#
#  Leave these function calls in place
#  The drive uses them to invoke actopn
def plan(): slice.plan()
def apply():slice.apply()
