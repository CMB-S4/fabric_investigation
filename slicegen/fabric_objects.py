"""

A collection of objects that provies resources in FABRIC for
CMB-S4 Phase one.

In fabric, a unit of provisioning is a *slice*.  For CMB-S4 a slice is
a collection of nodes and networks.  Nodes contain interfaces that are
attachend for networks.  A node with more than one interface is
usually on multiple networks.

A file of python object declaration is the configuration file. in The
configjuraion fike the user specifies a slice, and anhy number of
network and node objects. The configuration file processing program ,
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
networks then nodes.

The CMB_s4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  WHen
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
             
            

class Slice:
     # collect all the objects to make a slice
     # then 
     def __init__(self, name):
        self.name = name
        self.registered_nodes    = []
        self.registered_networks = []
        self.sleep_before_submit = 4
        
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
        time.sleep(self.sleep_before_submit)
        self.submit()

     def plan(self):
        show(self)
        for node in self.registered_nodes: node.plan()
        for network in self.registered_networks: network.plan()


class Node:
     def __init__ (self, slice, name, site, **kwargs):
          self.slice = slice
          self.name = name 
          self.site = site
          self.cores = 1
          self.ram   = 20
          self. disk = 10
          self.nics = {}
          if "image" in kwargs :  self.cores = kwargs["image"]
          if "cores" in kwargs :  self.cores = kwargs["cores"]
          if "ram"   in kwargs :  self.ram   = kwargs["ram"]
          if "disk"  in kwargs :  self.disk  = kwargs["disk"]
          self.slice.register_node(self)

     def add_nic(self, model, name):
          # Make the interface and record in the dictionary of all interfaces. 
          self.nics[name] = Nic(self, name, model)
        
     def get_nic(self, name):
          #return a nic object named name
          return self.nics[name]

     def apply():
          self.node = self.slice.add_node(name=self.name, site=self.site.name)
          self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
          self.node.set_image(self.image)
          #for nic in self.nics.keys():
          #    nic.iface = self.node.add_component(nic.model, nic.name).get_interfaces()[0]

     def plan(self):
          show(self)


class L2Network:
     def __init__(self, slice, name, niclist, **kwargs):
          self.name = name
          self.niclist = niclist
          self.slice = slice
          self.network = None
          self.subnet = self.random_IPV6_subnet()
          if "subnet" in kwargs :  self.subnet = kwargs["subnet"]
          self.slice.register_network(self)
    
     def apply(self):
          iflist = [n.iface for n in self.niclist]:
          for if in iflist:
               pass #assign an IF and IP address 
          self.network = self.slice.add_l2network(name=self.name, interfaces=niclist)
          

     def random_IPV6_subnet(self):
          import random
          x =  [int(random.random()*9999) for i in range(3)]
          x = "{}:{}:{}/64".format(*x)
          return x
     
     def plan(self):
          show(self)


class Nic:
     def __init__ (self, node , name, model):
          self.name    = name
          self.model   = model
          self.node    = node
          self.iface   = None
     def plan(self):
          show(self)




