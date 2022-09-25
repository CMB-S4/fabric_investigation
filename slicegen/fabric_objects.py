"""

A collection of objects that provies resources in FABRIC for
CMB-S4 Phase one.

In fabric, a unit of provisioning is a *slice*.  For CMB-S4 a slice is
a collection of nodes and networks.  Nodes contain interfaces that are
attachend for networks.  A node with more than one interface is
usually on multiple networks. a "NIC" object describes tme means a
node uses to connect to a network,

A file of python object declaration is the configuration file. in The
configjuraion fike the user specifies a slice, and anhy number of
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
networks, nodes and nics.

The CMB_s4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  When
the demonstraton is done, the only action supported is to tear the
slice down.

"""
def show(object):
     types = [type(1),type(None),type(True),type(""), type(1.0) ]
     items = vars(object)
     print (items["name"])
     for (key, value) in items.items():
        if key == "name" : continue
        if type(value) in types:
                print ("\t{}:{}".format(key, value))
        elif type(value) == type([]):
                print("\t{} {}".format(key, [v.name  for v in  value]))
        elif  type(value) == type({}):
                print("\t{} {}".format(key, value.keys()))
             
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
               if type(value) in types:
                    print ("\t{}:{}".format(key, value))
               elif type(value) == type([]):
                    print("\t{} {}".format(key, [v.name  for v in  value]))
               elif  type(value) == type({}):
                    print("\t{} {}".format(key, value.keys()))
               else:
                    print("\t{} {}".format(key, value.keys()))

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
        self.delay = 4
        if "delay"  in kwargs :  self.delay  = kwargs["delay"]
        
     def register_node(self, node):
        self.registered_nodes.append(node)
        
     def register_network(self, network):
        self.registered_networks.append(network)
        
     def submit(self):
        self.slice = fablib.new_slice(name=self.name)
        for network in self.registered_networks:
            network.declare()
        for node in self.registered_nodes:
            node.declare()
        time.sleep(self.delay)
        self.submit()

     def plan(self):
        show(self)
        for node in self.registered_nodes: node.plan()
        for network in self.registered_networks: network.plan()


class Node(Fabric_Base):
     """
     Create a Node, and specify non-network resources for the node.

     slice  - slice object
     name   - unique human-readbale name of node
     image  - Operataing system image to load on node
     
     Kwargs:
     - cores -- Number of cores for node (def 20)
     - ram   -- GB of ram for the node   (def 40)
     - dIsk  -- GB of DIsk for the node  (def 100)
     - site  -- FABRIC site for the node.(def NCSA)

 
     """
     def __init__ (self, slice, name, image, **kwargs):
          self.slice = slice
          self.name  = name
          self.image = image
          self.site  = kwargs.get("site"  , "NCSA")
          self.cores = kwargs.get("cores" , 20)
          self.ram   = kwargs.get("ram"   , 40)
          self.disk  =  kwargs.get("disk" , 100)
          self.nics  = {}
          self.slice.register_node(self)

     def add_nic(self, model, name):
          # Make the interface and record in the dictionary of all interfaces. 
          self.nics[name] = Nic(self, name, mode, network_namal)

     def apply():
          self.node = self.slice.add_node(name=self.name, site=self.site.name)
          self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          self.node.set_image(self.image)
          #for nic in self.nics.keys():
          #    nic.iface = self.node.add_component(nic.model, nic.name).get_interfaces()[0]

     def plan(self):
          show(self)


class L2Network(Fabric_Base):
     """
     Create a L2  Network, with an IPV6 address space
      
     slice  - slice object
     name   - unique human-readable name of network

     Kwargs:
     - subnet -- IPV6 subnet (def:random/64 subnet)
     
     """
     def __init__(self, slice, name,  **kwargs):
          self.slice = slice
          self.name = name
          self.network = None
          self.subnet = self.random_IPV6_subnet()
          if "subnet" in kwargs :  self.subnet = kwargs["subnet"]
          self.slice.register_network(self)
    
     def apply(self):
          iflist = [n.iface for n in self.niclist]
          for iface in iflist:
               pass #assign an IF and IP address 
          self.network = self.slice.add_l2network(name=self.name, interfaces=niclist)
          

     def random_IPV6_subnet(self):
          import random
          x =  [int(random.random()*9999) for i in range(3)]
          x = "{}:{}:{}/64".format(*x)
          return x
     
     def plan(self):
          show(self)


class Nic(Fabric_Base):
     """
     Bind a  Network interface card to a node and a netwwork

     slice   - slice object owningn th NIC
     name    - unique human-readable name of NIC
     node    - node object NIC is associated with
     network - network object NIC is associated with 

     Kwargs:
     - model -- NIC model (def NIC_Basic))
     """
     def __init__ (self, slice,  node, network, **kawrgs):
          self.name    = name
          self.node    = node
          self.network = network
          self.model   = kwargs.get("model", "NIC_Basic")

     def plan(self):
          show(self)




