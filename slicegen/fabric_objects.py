#!/usr/local/bin/python
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
the nic interfaces when they are created.)

The CMB_s4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  When
the demonstraton is done, the only action supported is to tear the
slice down.

"""
# https://github.com/fabric-testbed/jupyter-examples/blob/master/fabric_examples/public_demos/KNIT5/KNIT5_Creating_FABnet_Networks/KNIT5_Tutorial_Creating_FABnet_Networks.ipynb

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
     A base class for all objects in config file
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

     When Declaring, cause the objects to make relevent calls
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

          #
          # Make API calls to declate needed resources to FABRIC
          #
          for cfnode    in self.registered_cfnodes:    cfnode.declare()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.declare()
          for cfnic     in self.registered_cfnics:     cfnic.declare()
          
          #
          # submit -- casues declated recourses to  be realized.
          #
          time.sleep(self.delay)
          t0 = time.time()
          logging.info(f"submitting slice {self.name}")
          import pdb;pdb.set_trace()
          self.slice.submit()
          duration = time.time() - t0
          logging.info(f"submit complete in {duration} seconds")

          #
          # Configure -- configure realized resoruces
          #
          
          for cfnetwork in self.registered_cfnetworks: cfnetwork.configure()
          for cfnode in self.registered_cfnodes: cfnode.configure()
          for cfcmd     in self.registered_cfcmds:     cfcmd.configure()
          self.declare()

     def plan(self):
          self.show()
          for cfnode in self.registered_cfnodes:       cfnode.plan()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.plan()
          for cfnic     in self.registered_cfnics:     cfnic.plan() 
          for cfcmd     in self.registered_cfcmds:     cfcmd.plan()

     def declare(self):
          """
          For every node, loop though all the networks and set..
          route to the gateway on evey node on a differnt netowork.
          """

          import pdb ; pdb.set_trace()
          for this_cfnic in self.registered_cfnics:
               this_node =  this_cfnic.get_node()
               this_network_cfid = this_cfnic.cfnetwork.get_cfid()
               for other_cfnic in self.registered_cfnics:
                    other_network_cfid = other_cfnic.cfnetwork.get_cfid()
                    if this_network_cfid == other_network_cfid : continue
                    this_gateway = this_cfnic.get_network().get_gateway()
                    other_subnet = other_cfnic.get_network().get_subnet()
                    this_node.ip_route_add(subnet=other_subnet, gateway=this_gateway)   
     


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
          self.image = image
          self.site  = kwargs.get("site"  , "NCSA")
          self.cores = kwargs.get("cores" , 20)
          self.ram   = kwargs.get("ram"   , 40)
          self.disk  = kwargs.get("disk" , 100)
          self.cfnics  = []
          self.cfslice.register_cfnode(self)

     def get_node(self):
          node =  self.cfslice.slice.get_node(self.name)
          return node
     
     def declare(self):
          logging.info(f"creating node {self.name}")
          slice = self.cfslice.slice
          node = slice.add_node(name=self.name, site=self.site)
          self._declate_node = node
          node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          node.set_image(self.image)
          for index, cfnic  in  enumerate(self.cfnics):
               #import pdb; pdb.set_trace()
               node.add_component(model=cfnic.model, name=cfnic.name).get_interfaces()[index]
               cfnic.interface_index = index


     def configure(self):
          for cfnic in self.cfnics:
               #nodes
               interface = cfnic.get_interface()
               self.dev = interface.get_os_interface()
               cfnic.ip  = cfnic.cfnetwork.get_next_ip()
               interface.ip_addr_add(addr=cfnic.ip, subnet=cfnic.get_network().get_subnet())
               logging.info (f'{self.site}.{self.name}.{cfnic.ip}')
               
     def register_cfnic(self, nic):
          self.cfnics.append(nic)

     def plan(self):
          self.show()

               
class CfL3Network(CfFabric_Base):

     
     def __init__(self, cfslice, name, **kwargs):
          
          self.cfslice = cfslice  #Slice wrapper object 
          self.name = name
          self.cfnics = []
          self.subnet = None
          self.gateway = None
          self.cfslice.register_cfnetwork(self)
          self.available_ips  = []

     def declare(self):
          logging.info(f"creating L3 network {self.name}")
          slice = self.cfslice.slice
          interfaces = [cfnic.get_interface() for cfnic in self.cfnics]
          network = slice.add_l3network(name=self.name, interfaces=interfaces, type='IPv4')
          
     def get_network(self):
          return self.cfslice.slice.get_network(self.name)
          
     def register_cfnic(self, nic):
          self.cfnics.append(nic)

     def configure(self):
          # Get our gateway. -- network
          slice = self.cfslice.slice
          network = slice.get_network(name=self.name)
          self.subnet         = network.get_subnet()
          self.gateway        = network.get_gateway()
          # flatten generator to list.
          for h in self.subnet.hosts() : self.available_ips.append(h)
          self.available_ips.pop(0) # give out the gateway, remove it.
          logging.info(f"network,subnet,gateway,1st IP: {self.name},{self.subnet},{self.gateway},{self.available_ips[0]}...")
          pass
     
     def get_next_ip(self):
          return self.available_ips.pop(0)

     def get_cfid(self):
          network = self.get_network()
          return f'{network.get_site()}.{network.get_layer()}.{network.get_name()}'

          
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
    
     def declare(self):
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
     cfslice         - slice object owning th NIC
     name            - unique human-readable name of NIC
     cfnode          - node object NIC is associated with
     cfnetwork       - network object NIC is associated with
     interface_index - index into the nodes interface array

     Kwargs:
     - model -- NIC model (def NIC_Basic))
       mtu   -- max packet size (def = 1500)
     """
     def __init__ (self, cfslice,  name,  cfnode, cfnetwork, **kwargs):
          self.name              = name  # name of NIC
          self.cfslice           = cfslice
          self.cfnode            = cfnode
          self.cfnetwork         = cfnetwork
          self.model             = kwargs.get("model", "NIC_Basic")
          self.interface_index   = None  #known after declare.
          self.mtu               = kwargs.get("mtu", "1500")
          self.cfnode.register_cfnic(self)      #tell the cfnode about the NIC
          self.cfnetwork.register_cfnic(self)   #Tell   the cfnet about the  NIC
          cfslice.register_cfnic(self)          #Tell our cfslice about the NIC

     def get_node(self):          
          return self.cfnode.get_node()

     def get_network(self):
          return self.cfnetwork.get_network()

     def get_interface(self):
          return self.get_node().get_interfaces()[self.interface_index]
          
     def plan(self):
          self.show()

     def declare(self):
          # no actions here as this is just encapusulated info to share
          # NODES and Networks use this info in their declare() steps
          pass

     
class CfCmds(CfFabric_Base):
     """
     Commands to send to a node as root.

     slice  - slice object 
     name   - Memonic name for this code (Need not be unique)
     node   - node object to execute command on
     cmds   - command text to execute, multiple lines allowed)
              n.b open("cmds,txt","r").read() is an idiom....
              ... to read commands from a file.
     
     kwargs :
           none (yet)
     """

     def __init__ (self, slice, cmdname, cfnode, cmds, **kwargs):
          self.slice = slice
          self.name     = cmdname  #all objetcs need a "name".
          self.cfnode   = cfnode
          self.cmds     = cmds
          self.stdout   = None
          self.stderr   = None
          slice.register_cfcmds(self) # tell our slice about the commands

     def plan(self):
          self.show()

     def configure(self):
          node = self.cfnode.get_node()
          (self.stdout, self.stderr) = node.execute(self.cmds)
          print (f"{self.name} {node}: stdout...\n {self.stdout}")
          print (f"{self.name} {node}: stderr...\n {self.stderr}")


