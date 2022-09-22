class Slice:
    def __init__(self, name):
        self.name = name
        self.registered_nodes    =[]
        self.registered_networks =[]
        
    def register_node(self, node):
        self.registered_nodes.append(node)
        
    def self.register_network(self, network):
        self.registered_networks.append(network)
        
    def submit():
        for node in self.registered_nodes:
            node.declare()
        for network in self.registered_networks:
            network.declare()
        self.submit()
    

class Node:
    def __init (self, slice, name, site, **kwargs):
        drlf.slice = slice
        self.name = name 
        self.site = site
        self.cores = 1
        self.ram   = 20
        self. disk = 10
        self.ifaces = {}
        self.image = None
        if "cores" in kwargs :  self.cores = kwargs["cores"]
        if "ram"   in kwargs :  self.ram   = kwargs["ram"]
        if "disk"  in kwargs :  self.disk  = kwargs["disk"]
        self.slice.register_node(self)

    def add_iface(self, model, name):
        # Make the interface and record in the dictionary of all interfaces. 
        iface = self.node.add_compoment((model=model, name=).get_interfaces()[0])
        self.iface[name] = {"iface" : iface ; "model" ; model}]
                                          
    def declare()
        self.node = self.slice.add_node(name=self.name, site=self.site.name)
        self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
        self.node.set_image(self.image)

class L2Network:
    def __init__(self, slice, anem niclist=[]):
        self.name = name
        self.niclist = niclist
        self.slice.register_node(self)
        
    def declare(self):
        net1 = self.slice.add_l2network(name=self.name, interfaces=[iface1, iface2])
        


#
#   use of this 
IMAGE = 'default_rocky_8'

s = Slice('MySliceSep12B')
node1 = Node(s, 'CMBS4Node_ncsa1', 'NCSA',
              disk=1, cores=2, ram=10, image=image)
node1.add_nic('NIC_Basic', 'GP') #general purpose NIC

node2 = Node(s, 'CMBS4Node_tacc2', 'TACC',
              disk=1, cores=2, ram=10, image=image)
node1.add_nic('NIC_Basic', 'GP') #general purpose NIC

net1 = L2Network(s, 'net1',[node1.get_nic("GP"), node2.get_nic("GP")])

s.submit()
