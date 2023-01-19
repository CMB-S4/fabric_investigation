#!/usr/bin/env python
""" collection of objects that provides resources in FABRIC for
CMB-S4 Phase one testing.

The CMB-S4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  When
the demonstraton is done, the only action supported is to tear the
slice down.

In FABRIC, a unit of provisioning is a *slice*.  For CMB-S4 a slice is
a collection of nodes and networks.  A FABRIC site contains nodes
and networks. Routes between site networks allow data to be sent
between nodes on differnet sites.

fabric_objects allow CMB-S4 to create and use a topology of nodes
and networks supporting the project's "prompt" use case. THree objects
 are used to instaniate FABRIC resources: 1)A CfNode objects describe nodes.
2) CfNetwork objects descibe networks. 3) CfNic objects describe how nodes
connect to networks. Additionally, CfCmds objects send commands to nodes.
(however use planner.py to send lareg number of commands to nodes)

A file of python object declarations is the configuration file. In the
configuration file the user specifies a slice, and any number of
network, node and nic objects. The configuration file processing
program , *planner.py* will import the configuraaion file and cause
the objects to be instantated.

apply"Plan level" prints out, in human readable form, a good deal of
information about what would be instantiated. This output helps an
author determine whether the configuration is what was intended, and can
serve to document the configuration.  Planning does not allocate
resources in FABRIC, and does not cause any FABRIC API's to be called.
i.e. A user running at Plan level need not be credentialed to access
FABRIC.

"Apply level" repeats the steps of planning, and then calls FABRIC
APIS to instantiate the plan. A slice object is instantiated,
nodes, then networks are declared to FABRIC. The FABRIC infrastructre
realizes the declared system in hardware. Live Networks and Nodes
are configured. Finally, Routes are establised between all nodes
and all networks. Finally any commands are issued in the order they
were declared.

planner.py is available to access the nodes, tear down the system
and perform other operations.

"""
# https://github.com/fabric-testbed/jupyter-examples/blob/master/fabric_examples/public_demos/KNIT5/KNIT5_Creating_FABnet_Networks/KNIT5_Tutorial_Creating_FABnet_Networks.ipynb

from fabrictestbed.slice_manager import SliceManager, Status, SliceState
from fabrictestbed_extensions.fablib.fablib import fablib
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network
import time
import logging

from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
fablib = fablib_manager()             
#fablib.show_config()

class CfFabric_Base:
     """
     A base class for all objects in config file
     """
     scalar_types = [type(1),type(None),type(True),type(""), type(1.0) ]
     logger   = None  
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
                    
     def get_logger(self):
          import sys
          if  not CfFabric_Base.logger:
               CfFabric_Base.logger = logging.getLogger(sys.argv[0])
          return CfFabric_Base.logger
     
class CfSlice(CfFabric_Base):
     """
     Collect the nodes and networks for a slice.

     When planning cause the objects  to print information.

     When applyingg, cause the objects to make relevent calls
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
          """ remember every cfnode """
          self.registered_cfnodes.append(cfnode)
        
     def register_cfnetwork(self, cfnetwork):
          """ remember every cfnetwork """
          self.registered_cfnetworks.append(cfnetwork)

     def register_cfnic(self, cfnic):
          """ remember every cfnic """
          self.registered_cfnics.append(cfnic)

     def register_cfcmds(self,cfcmds):
          """ remember every cfcmds """ 
          self.registered_cfcmds.append(cfcmds)
        
     def apply(self):
          """ cause the slice to be realized """
          self.get_logger().info(f"instatiate clice {self.name}")       
          self.slice = fablib.new_slice(name=self.name)

          #
          # Make API calls to declate needed resources to FABRIC
          # Nodes first....
          for cfnode    in self.registered_cfnodes:    cfnode.declare()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.declare()
          for cfnic     in self.registered_cfnics:     cfnic.declare()
          
          #
          # submit -- relalize these resources in fabric..
          #
          time.sleep(self.delay) #addtional settling time
          t0 = time.time()
          self.get_logger().info(f"submitting slice {self.name}")
          self.slice.submit()
          duration = time.time() - t0
          self.get_logger().info(f"submit complete in {duration} seconds")


          #
          # Deal with a problem ni rocky linux, per forum reply from
          # Ilya, and mail from Greg Nov 4 2022.
          self.get_logger().info(f"beginning rocky linux network problem work around")
          for node in self.slice.get_nodes():
               node.network_manager_start()    
          for iface in self.slice.get_interfaces():
             iface.get_node().execute(f'sudo nmcli device set {iface.get_device_name()} managed no')   
          self.get_logger().info(f"end rocky linux network problem work around")


          #
          # Configure -- configure the realized resoruces
          # networks first. But for a quirk in fabric, reboot the nodes
          # before configuring networks, and wait for the nodes to come up
          # now setup networks. to the IP level.
          print(self.slice)
          print(self.name)
          #self.slice = fablib.new_slice(name=self.name) #refresh after submit.
          print(self.slice)
          for cfnetwork in self.registered_cfnetworks: cfnetwork.configure()
          for cfnode in self.registered_cfnodes:       cfnode.configure()
          for cfcmd     in self.registered_cfcmds:     cfcmd.configure()
          self.configure()

     def plan(self):
          """
          Print the objects and their relationships out.
          """
          
          self.show()
          for cfnode in self.registered_cfnodes:       cfnode.plan()
          for cfnetwork in self.registered_cfnetworks: cfnetwork.plan()
          for cfnic     in self.registered_cfnics:     cfnic.plan() 
          for cfcmd     in self.registered_cfcmds:     cfcmd.plan()

     def configure(self):
          """
          For every node, confgure a route to every other subnet in this slice.
          print out the digest file. 
          make a digest -- list of (network_name, subnets)
          """
 
          #self.slice = fablib.new_slice(name=self.name) #dlp
          for this_cfnic in self.registered_cfnics:
               this_node_name         = this_cfnic.get_node().get_name()
               this_network_name      = this_cfnic.get_network().get_name()
               for a_cfnic in self.registered_cfnics:
                    if a_cfnic.get_network().get_name() == this_network_name :
                         #routes not needed between nodes on same net.
                         continue
                    # make a route to a non-native network
                    a_subnet  = a_cfnic.get_network().get_subnet()
                    gateway   = this_cfnic.get_network().get_gateway()
                    node      = this_cfnic.get_node()
                    node.ip_route_add(subnet=a_subnet, gateway=gateway)
                    #log it
                    node_name = node.get_name()
                    net_name  = a_cfnic.get_network().get_name()
                    self.get_logger().info(f"routing node {node_name} to network {net_name}"
                                 )
          with open(f"{self.name}.digest","w") as f:
               for cfnic in self.registered_cfnics:
                    node_name = cfnic.get_node().get_name()
                    ip_address = cfnic.ip
                    f.write(f"{node_name} {ip_address}\n")


class CfNode(CfFabric_Base):
     """
     Create a Node, and specify non-network resources for the node.

     slice  - slice object
     name   - unique human-readbale name of node
     image  - Operating system image to load on node
     
     Kwargs:
     - cores -- Number of cores for node (def 20)
     - ram   -- GB of ram for the node   (def 40)
     - disk  -- GB of Disk for the node  (def 100)
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
          """
          Return a valid node object. Each call returns
          a new FABRIC python object, which acts on the
          same underlying FABRIC node
          """
          node =  self.cfslice.slice.get_node(self.name)
          return node
     
     def declare(self):
          """
          get a node of required capacity; attach NICS
          """
          self.get_logger().info(f"declaring  node {self.name}")
          slice = self.cfslice.slice
          node = slice.add_node(name=self.name, site=self.site)
          self._declate_node = node
          node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          node.set_image(self.image)
          for index, cfnic  in  enumerate(self.cfnics):
               node.add_component(model=cfnic.model, name=cfnic.name).get_interfaces()[index]
               cfnic.interface_index = index


     def configure(self):
          """
          Bind NICS to network. Bind IPaddress to Nic. 
          """
          # e,g self.get_node().execute("date")
          for cfnic in self.cfnics:
               #nodes
               interface = cfnic.get_interface()
               self.dev  = interface.get_os_interface()
               cfnic.ip  = cfnic.cfnetwork.get_next_ip()
               interface.ip_addr_add(addr=cfnic.ip, subnet=cfnic.get_network().get_subnet())
               self.get_logger().info (f'{self.site}.{self.name}.{cfnic.ip}')
               
     def register_cfnic(self, nic):
          """
          Remember all NICS
          """
          self.cfnics.append(nic)

     def plan(self):
          """
          print informatkon about the node and its relatiionsships out
          """
          self.show()

     def reboot(self):
          """
          Reboot the node
          """
          self.get_logger().info(f"rebooting {self.name}")
          (stdout, stderr) = self.get_node().execute("sudo reboot")
          print ("reboot: stdout, sterr:", stdout, stderr)
          
     def wait_reboot(self):
          """ 
          a successful command assured that the node has rebooted
          """
          self.get_logger().info(f"waiting complets reboot of  {self.name}")
          t0 = time.time()
          for retry in range(5):
               stdout, stdin = self.get_node().execute("systemctl is-system-running")
               # either of the answer below indicate that systemd  as finished ...
               # starting stuff The hope is the nodes are not stable. 
               if "degraded" in stdout : break  # normal successful path when developng this.
               if "running"  in stdout : break  # ideal, but not observed
               time.sleep(20)
          elapsed = int(time.time() - t0)
          self.get_logger().info(
               f"{self.name} is up elapsed time for check: {elapsed}, is-system-running: {stdout}"
          )
          
class CfL3Network(CfFabric_Base):
     """
     Create a IPV4 L3 network.

     slice  - slice object
     name   - unique human-readbale name of node
     image  - Operating system image to load on node
     
     Kwargs:
     None yets (type == IPV4, IPV6 envisioned.
     """
     
     def __init__(self, cfslice, name, **kwargs):
          
          self.cfslice = cfslice  #Slice wrapper object # goes
          self.name = name
          self.cfnics = []
          self.subnet = None
          self.gateway = None
          self.type = kwargs.get("type" , "IPv4")
          self.cfslice.register_cfnetwork(self)
          self.available_ips  = []

     def declare(self):
          """ declare network and interfaces on network """
          self.get_logger().info(f"declaring L3 network {self.name}")
          slice = self.cfslice.slice
          interfaces = [cfnic.get_interface() for cfnic in self.cfnics]
          network = slice.add_l3network(name=self.name, interfaces=interfaces, type=self.type)
          
     def get_network(self):
          """
          Return a valid network object. Each call returns
          a new FABRIC python object, which acts on the
          same underlying FABRIC network.
          """
          return self.cfslice.slice.get_network(self.name)
          
     def register_cfnic(self, nic):
          """Remember all the NICs for this network """
          self.cfnics.append(nic)

     def configure(self):
          """ Collect information the nodes will need. """
          # Get our gateway. -- network
          slice = self.cfslice.slice
          network = slice.get_network(name=self.name)
          self.subnet         = network.get_subnet()
          self.gateway        = network.get_gateway()
          # flatten generator to list.
          for h in self.subnet.hosts() : self.available_ips.append(h)
          self.available_ips.pop(0) # The gateway, is given, too remove it.
          self.get_logger().info(f"network,subnet,gateway,1st IP: {self.name},{self.subnet},{self.gateway},{self.available_ips[0]}...")
          pass\
     
     def get_next_ip(self):
          """ Get the next available IP """
          return self.available_ips.pop(0)

     def get_cfid(self):
          """ Give a unique identifire for this network""" 
          network = self.get_network()
          return f'{network.get_site()}.{network.get_layer()}.{network.get_name()}'

          
     def plan(self):
          """
          print informatkon about the network and its relationships out
          """
          self.show()


class CfL2Network(CfFabric_Base):
     """
     Create a L2  Network, with an IPV6 address space
     *** NOT TESTED NOT DEBUGGED ***
      
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
          self.get_logger().info(f"creating L2 network {self.name}")
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
          """
          print information about the nICand its relationships
          """
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
          """ Return FABRIC level node object"""
          return self.cfnode.get_node()

     def get_network(self):
          """ Return FABRIC level network object"""
          return self.cfnetwork.get_network()

     def get_interface(self):
          """ Return FABRIC level interfaaxe  object"""
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


