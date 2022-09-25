#
import fabric_objects as fo

# default quantiteis
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100

slice = fo.Slice('MySliceSep12B')

node1 = fo.Node(slice, 'CMBS4Node_ncsa1', 'NCSA',
                disk=disk, cores=cores, ram=ram, image=image)
node1.add_nic('NIC_Basic', 'GP') #general purpose NIC

node2 = fo.Node(slice, 'CMBS4Node_tacc2', 'TACC',
                              disk=disk, cores=cores, ram=ram, image=image)
node2.add_nic('NIC_Basic', 'GP') #general purpose NIC

net1 = fo.L2Network(slice, 'net1',[node1.get_nic("GP"), node2.get_nic("GP")])


#
#  
#

def plan(): slice.plan()
def apply():slice.apply()
