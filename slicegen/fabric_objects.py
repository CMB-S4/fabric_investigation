"""
A collection of objects that provides resources in FABRIC for
C-S4 Phase one.

In fabric, a unit of provisioning is a *slice*.  For CMB-S4 a slice is
a collection of nodes and networks.  Nodes contain interfaces that are
attachend for networks.  A node with more than one interface is
usually on multiple networks. a "NIC" object describes the means a
node uses to connect to a network and the network to connect to.

A file of python object declaration is the configuration file. in The
configuration file the user specifies a slice, and any number of
network node and nic  objects. The configuration file processing program ,
*Planner.py* will import and cause the objects to be instantated and
run at the  "plan" or "apply" Level.

"Plan level" prints out, in human readable form, a good deal of
information about what wuuld be instantiated. This output helps an
author determe whether the configuration is what was intended, and can
serve to document the configuration.  Planning does not allocate
resources in FABRIC, and does not cause any FABRIC API's to be called.
i.e. A user running at Plan level need not be credentialed to access
FABRIC.

"Apply level" repeats the steps of planning, and then calls FABRIC
APIS to instantiate the plan. A slice object is instantiated, then
nodes, nics and finally networks (which seem to need to knmw all
the nic interfaces when they are created.

The CMB_s4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  When
the demonstraton is done, the only action supported is to tear the
slice down.

"""

from fabrictestbed.slice_manager import SliceManager, Status, SliceState
from fabrictestbed_extensions.fablib.fablib import fablib
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network
import time
import logging

from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
fablib = fablib_manager()             
fablib.show_config()

class Fabric_Base:
     """
     a base clase for all objects in config file
     """
     scalar_types = [type(1),type(None),type(True),type(""), type(1.0) ]
          
     def show(self):
          items = vars(self)
          print (items["name"])
          for (key, value) in items.items():
               if key == "name" : continue
               if type(value) in self.scalar_types:
                    print ("\t{}:{}".format(key, value))
               elif type(value) == type([]):
                    print("\t{} {}".format(key, [v.name  for v in  value]))
               elif  type(value) == type({}):
                    print("\t{} {}".format(key, value.keys()))
               else:
                    print("\t{} {}".format(key, value))

class Slice(Fabric_Base):
     """
     Collect the nodes and networks for a slice.

     When planning cause the objects  to print information.

     When Applying, cause the objects to make relevent calls
     to the FABRIC APIS. When all objects are processed wait
     for *delay* seconds before calling  *submit*.

     Kwargs:
     - delay -- seconds to delay before calling submit.
     
     """
     # then 
     def __init__(self, name, **kwargs):
          self.name = name
          self.registered_nodes    = []
          self.registered_networks = []
          self.registered_nics     = []
          self.registered_cmds     = []
          self.delay = 4
          if "delay"  in kwargs :  self.delay  = kwargs["delay"]
        
     def register_node(self, node):
          self.registered_nodes.append(node)
        
     def register_network(self, network):
          self.registered_networks.append(network)

     def register_nic(self, nic):
          self.registered_nics.append(nic)

     def register_cmds(self,cmds):
          self.registered_cmds.append(cmds)
        
     def apply(self):
          logging.info(f"creating Slice {self.name}")       
          self.slice = fablib.new_slice(name=self.name)
          for node    in self.registered_nodes:    node.apply()
          for network in self.registered_networks: network.apply()
          for nic     in self.registered_nics:     nic.apply()
          time.sleep(self.delay)
          self.slice.submit()
          logging.info(f"submitted Slice {self.name}")       
          for cmd     in self.registered_cmds:     cmd.apply()

     def plan(self):
          self.show()
          for node in self.registered_nodes:       node.plan()
          for network in self.registered_networks: network.plan()
          for nic     in self.registered_nics:     nic.plan() 
          for cmd     in self.registered_cmds:     cmd.plan()


class Node(Fabric_Base):
     """
     Create a Node, and specify non-network resources for the node.

     slice  - slice object
     name   - unique human-readbale name of node
     image  - Operating system image to load on node
     
     Kwargs:
     - cores -- Number of cores for node (def 20)
     - ram   -- GB of ram for the node   (def 40)
     - dIsk  -- GB of DIsk for the node  (def 100)
     - site  -- FABRIC site for the node.(def NCSA)

 
     """
     def __init__ (self, slice, name, image, **kwargs):
          self.Slice = slice  #Slice wrapper object 
          self.name  = name
          self.node  = None
          self.image = image
          self.site  = kwargs.get("site"  , "NCSA")
          self.cores = kwargs.get("cores" , 20)
          self.ram   = kwargs.get("ram"   , 40)
          self.disk  =  kwargs.get("disk" , 100)
          self.nics  = []
          self.Slice.register_node(self)

     def apply(self):
          logging.info(f"creating node {self.name}")
          slice = self.Slice.slice
          self.node = slice.add_node(name=self.name, site=self.site)
          self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          self.node.set_image(self.image)
          for index, nic  in  enumerate(self.nics):
              nic.interface = self.node.add_component(nic.model, nic.name).get_interfaces()[index]

     def register_nic(self, nic):
          self.nics.append(nic)

     def plan(self):
          self.show()

class L3Network(Fabric_Base):

     def __init__(self, slice, name, **kwargs):
          
          self.Slice = slice  #Slice wrapper object 
          self.name = name
          self.network = None
          self.nics = []
          self.subnet = None
          self.gateway = None
          self.Slice.register_network(self)

     def apply(self):
          logging.info(f"creating L3 network {self.name}")
          import pdb; pdb.set_trace()
          slice = self.Slice.slice
          interfaces = [nic.interface for nic in self.nics]
          self.network = slice.add_l3network(name=self.name, interfaces=interfaces, type='IPv4')
          
     def register_nic(self, nic):
          self.nics.append(nic)
          
     def plan(self):
          self.show()
     
          
class L2Network(Fabric_Base):
     """
     Create a L2  Network, with an IPV6 address space
      
     slice  - slice object
     name   - unique human-readable name of network

     Kwargs:
     - subnet -- IPV6 subnet (def:random/64 subnet)
     
     """
     def __init__(self, slice, name,  **kwargs):
          self.Slice = slice  #Slice wrapper object 
          self.name = name
          self.network = None
          self.subnet = None
          self.subnet = self.random_IPV6_subnet()
          if "subnet" in kwargs :  self.subnet = kwargs["subnet"]
          self.nics = []
          self.Slice.register_network(self)
    
     def apply(self):
          logging.info(f"creating L2 network {self.name}")
          slice = self.Slice.slice
          interfaces = [n.interface for n in self.nics]
          self.network = slice.add_l2network(name=self.name, interfaces=interfaces)
          fabric_subnet_object  = IPv6Network(self.subnet)
          available_ips = fabric_subnet_object.hosts()
          for nic in self.nics:
               IpV6_addr = next(available_ips)
               nic.interface.ip_addr_add(addr=IpV6_addr, subnet=fabric_subnet_object)
               nic.interface.set_ip(ip= IpV6_addr, mtu=nic.mtu) 

     def random_IPV6_subnet(self):
          import random
          x =  [int(random.random()*9999) for i in range(2)]
          x = "{}:{}::/64".format(*x)
          return x

     def register_nic(self, nic):
          self.nics.append(nic)

          
     def attach_interface(self, interface):
          self.interfaces.append(interface)
     
     def plan(self):
        self.show()
          


class Nic(Fabric_Base):
     """
     Bind a  Network interface card to a node and a L2 or L3  netwwork
     slice   - slice object owningn th NIC
     name    - unique human-readable name of NIC
     node    - node object NIC is associated with
     network - network object NIC is associated with 

     Kwargs:
     - model -- NIC model (def NIC_Basic))
       mtu   -- max packet dise (def = 1500)
     """
     def __init__ (self, slice,  name,  node, network, **kwargs):
          self.name      = name  # name of NIC
          self.node      = node
          self.network   = network
          self.model     = kwargs.get("model", "NIC_Basic")
          self.interface = None  #known after apply.
          self.mtu       = kwargs.get("mtu", "1500")
          self.node.register_nic(self)      #tell the node about the NIC
          self.network.register_nic(self)   #Tell   the net about the  NIC
          slice.register_nic(self)          # tell our slic about the NIC
          
     def plan(self):
          self.show()

     def apply(self):
          # no actions here as this is just encapusulated info to share
          # NODES and Networks use this info in their apply() steps
          pass


class Cmds(Fabric_Base):
     """
     Commands to send to a node as root.

     slice  - slice object owning the node.
     name   - Memonic name for this code (Need not be unique)
     node   - node object to executre command on
     cmds   - command text to execute, multiple lines allowed)
              n.b open("cmds,txt","r").read() is an idiom....
              ... to read commands from a file.
     
     kwargs :
           none (yet)
     """

     def __init__ (self, slice, name, node, cmds, **kwargs):
          self.slice = slice
          self.name   = name
          self.node   = node
          self.cmds   = cmds
          self.stdout = None
          self.stderr = None
          slice.register_cmds(self) # tell out slic about the commands

     def plan(self):
          self.show()

     def apply(self):
          import pdb; pdb.set_trace()
          node = self.node.node
          (self.stdout, self.stderr) = node.execute(self.cmds)


