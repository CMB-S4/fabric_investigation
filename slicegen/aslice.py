import fabric_objects as fo


# default quantiteis
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



#
#  
#

def plan(): slice.plan()
def apply():
    slice.apply()
