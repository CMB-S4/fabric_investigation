
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

class CfFabric_Base:
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

     
class CfSlice(CfFabric_Base):
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
          self.registered_cfnodes    = []
          self.registered_cfnetworks = []
          self.registered_cfnics     = []
          self.registered_cfcmds     = []
          self.delay = 4
          if "delay"  in kwargs :  self.delay  = kwargs["delay"]
        
     def register_cfnode(self, cfnode):
          self.registered_cfnodes.append(cfnode)
        
     def register_cfnetwork(self, cfnetwork):
          self.registered_cfnetworks.append(cfnetwork)

     def register_cfnic(self, cfnic):
          self.registered_cfnics.append(cfnic)

     def register_cfcmds(self,cfcmds):
          self.registered_cfcmds.append(cfcmds)
        
     def apply(self):
          logging.info(f"instatiate clice {self.name}")       
          self.slice = fablib.new_slice(name=self.name)
          for cfnode    in self.registered_cfnodes:    cfnode.apply()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.apply()
          for cfnic     in self.registered_cfnics:     cfnic.apply()
          time.sleep(self.delay)
          t0 = time.time()
          logging.info(f"submitting slice {self.name}")
          self.slice.submit()
          duration = time.time() - t0
          logging.info(f"submit complete in {duration} seconds")
          import pdb; pdb.set_trace()
          #reak by using the same  name.
          logging.info(f"begin post submit for {len(self.registered_cfnetworks)} networks")
          for cfnetwork in self.registered_cfnetworks: cfnetwork.post_submit()
          logging.info(f"begin post submit for {len(self.registered_cfnodes)} nodes")
          for cfnode in self.registered_cfnodess: cfnode.post_submit()
          for cfcmd     in self.registered_cfcmds:     cfcmd.apply()

     def plan(self):
          self.show()
          for cfnode in self.registered_cfnodes:       cfnode.plan()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.plan()
          for cfnic     in self.registered_cfnics:     cfnic.plan() 
          for cfcmd     in self.registered_cfcmds:     cfcmd.plan()


class CfNode(CfFabric_Base):
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
     def __init__ (self, cfslice, name, image, **kwargs):
          self.cfslice = cfslice  #Slice wrapper object 
          self.name  = name
          self.node  = None
          self.image = image
          self.site  = kwargs.get("site"  , "NCSA")
          self.cores = kwargs.get("cores" , 20)
          self.ram   = kwargs.get("ram"   , 40)
          self.disk  =  kwargs.get("disk" , 100)
          self.cfnics  = []
          self.cfslice.register_cfnode(self)

     def apply(self):
          logging.info(f"creating node {self.name}")
          slice = self.cfslice.slice
          self.node = slice.add_node(name=self.name, site=self.site)
          self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          self.node.set_image(self.image)
          for index, cfnic  in  enumerate(self.cfnics):
               #import pdb; pdb.set_trace()
               cfnic.interface = self.node.add_component(model=cfnic.model, name=cfnic.name).get_interfaces()[index]

     def post_submit(self):
          import pdb; pdb.set_trace()
          for cfnic in self.cfnics:
               #nodes
               self.dev = cfnic.interface.get_os_interface()
               self.ip  = cfnic.network.get_available_ips()[0]
               cfnic.interface.ip_addr_add(addr=self.ip, subnet=cfnic.network.subnet)
               
     def register_cfnic(self, nic):
          self.cfnics.append(nic)

     def plan(self):
          self.show()


class CfRouteAll(CfFabric_Base):
     # 1) for all L3 interfaces -- assign gateway and subnet to its ...
     # ... associated network using its post_submit method. 
     # 2)  for every node, establish "os interface" and assign an IP ...
     # ... address. using its post_submit method.
     # 3) using the of all nodes in the slice, for every pair of nodes ..
     # .... (on different nets?) establish mutual routes to each other

     def apply(self):
          pass
               

               
class CfL3Network(CfFabric_Base):

     def __init__(self, cfslice, name, **kwargs):
          
          self.cfslice = cfslice  #Slice wrapper object 
          self.name = name
          self.network = None
          self.cfnics = []
          self.subnet = None
          self.gateway = None
          self.cfslice.register_cfnetwork(self)

     def apply(self):
          logging.info(f"creating L3 network {self.name}")
          import pdb; pdb.set_trace()
          slice = self.cfslice.slice
          interfaces = [cfnic.interface for cfnic in self.cfnics]
          self.network = slice.add_l3network(name=self.name, interfaces=interfaces, type='IPv4')

          
     def register_cfnic(self, nic):
          self.cfnics.append(nic)

     def post_submit(self):
          #netowrk
          import pdb; pdb.set_trace()
          self.network = slice.get_network(name=self.name)
          network   = [cfnic.cfnetwork.network for cfnic in self.cfnics]
          for interface in interfaces:
               self.subnet  = network.get_subnet()
               self.gateway = network.get_gateway()

          
     def plan(self):
          self.show()


class CfL2Network(CfFabric_Base):
     """
     Create a L2  Network, with an IPV6 address space
      
     slice  - slice object
     name   - unique human-readable name of network

     Kwargs:
     - subnet -- IPV6 subnet (def:random/64 subnet)
     
     """
     def __init__(self, slice, name,  **kwargs):
          self.cfslice = slice  #Slice wrapper object 
          self.name = name
          self.network = None
          self.subnet = None
          self.subnet = self.random_IPV6_subnet()
          if "subnet" in kwargs :  self.subnet = kwargs["subnet"]
          self.cfnics = []
          self.cfslice.register_cfnetwork(self)
    
     def apply(self):
          logging.info(f"creating L2 network {self.name}")
          slice = self.cfslice.slice
          interfaces = [n.interface for n in self.nics]
          self.network = slice.add_l2network(name=self.name, interfaces=interfaces)
          fabric_subnet_object  = IPv6Network(self.subnet)
          available_ips = fabric_subnet_object.hosts()
          for cfnic in self.cfnics:
               IpV6_addr = next(available_ips)
               cfnic.interface.ip_addr_add(addr=IpV6_addr, subnet=fabric_subnet_object)
               cfnic.interface.set_ip(ip= IpV6_addr, mtu=nic.mtu) 

     def random_IPV6_subnet(self):
          import random
          x =  [int(random.random()*9999) for i in range(2)]
          x = "{}:{}::/64".format(*x)
          return x

     def register_cfnic(self, nic):
          self.cfnics.append(nic)

     def attach_interface(self, interface):
          self.interfaces.append(interface)
     
     def plan(self):
        self.show()
          


class CfNic(CfFabric_Base):
     """
     Bind a  Network interface card to a node and a L2 or L3  netwwork
     cfslice   - slice object owningn th NIC
     name    - unique human-readable name of NIC
     cfnode    - node object NIC is associated with
     cfnetwork - network object NIC is associated with 

     Kwargs:
     - model -- NIC model (def NIC_Basic))
       mtu   -- max packet dise (def = 1500)
     """
     def __init__ (self, cfslice,  name,  cfnode, cfnetwork, **kwargs):
          self.name      = name  # name of NIC
          self.cfslice   = cfslice
          self.cfnode    = cfnode
          self.cfnetwork = cfnetwork
          self.model     = kwargs.get("model", "NIC_Basic")
          self.interface = None  #known after apply.
          self.mtu       = kwargs.get("mtu", "1500")
          self.cfnode.register_cfnic(self)      #tell the cfnode about the NIC
          self.cfnetwork.register_cfnic(self)   #Tell   the cfnet about the  NIC
          cfslice.register_cfnic(self)            # tell our cfslice about the NIC
          
     def plan(self):
          self.show()

     def apply(self):
          # no actions here as this is just encapusulated info to share
          # NODES and Networks use this info in their apply() steps
          pass


class CfCmds(CfFabric_Base):
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

     def __init__ (self, slice, cfname, cfnode, cmds, **kwargs):
          self.slice = slice
          self.cfname   = name
          self.cf.node   = node
          self.cfcmds   = cmds
          self.stdout = None
          self.stderr = None
          slice.register_cfcmds(self) # tell out slic about the commands

     def plan(self):
          self.show()

     def apply(self):
          import pdb; pdb.set_trace()
          node = self.cfnode.node
          (self.stdout, self.stderr) = node.execute(self.cmds)


