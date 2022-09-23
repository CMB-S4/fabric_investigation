#
import fabric_objects as fo
#   use of this 
IMAGE = 'default_rocky_8'

slice = fo.Slice('MySliceSep12B')

node1 = fo.Node(slice, 'CMBS4Node_ncsa1', 'NCSA',
              disk=1, cores=2, ram=10, image=IMAGE)
node1.add_nic('NIC_Basic', 'GP') #general purpose NIC

node2 = fo.Node(slice, 'CMBS4Node_tacc2', 'TACC',
              disk=1, cores=2, ram=10, image=IMAGE)
node2.add_nic('NIC_Basic', 'GP') #general purpose NIC

net1 = fo.L2Network(slice, 'net1',[node1.get_nic("GP"), node2.get_nic("GP")])


#
#  
#

def plan(): slice.plan()
def apply():slice.apply()
