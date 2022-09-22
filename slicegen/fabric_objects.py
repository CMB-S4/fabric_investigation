
image = "rockyLinux"

class Slice:
    # collect all the objects to make a slice
    # then 
    def __init__(self, name):
        self.name = name
        self.registered_nodes    =[]
        self.registered_networks =[]
        
    def register_node(self, node):
        self.registered_nodes.append(node)
        
    def register_network(self, network):
        self.registered_networks.append(network)
        
    def submit(self):
        self.slice = fablib.new_slice(name=self.name)
        for node in self.registered_nodes:
            node.declare()
        for network in self.registered_networks:
            network.declare()
        self.submit()

    def show(self):
        import pprint
        pprint.pprint(var(self))
        for node in self.registered_nodes: node.show()
        for network in self.registered_networks: network.show()


class Node:
    def __init__ (self, slice, name, site, **kwargs):
        self.slice = slice
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

    def add_nic(self, model, name):
        # Make the interface and record in the dictionary of all interfaces. 
        self.ifaces[name] = {"model" : model}
        
    def get_iface(self, name):
        import pdb; pdb.set_trace()
        return self.ifaces[name]["iface"]

    def show(self):
        import pprint
        pprint.pprint(var(self))

    def declare():
        self.node = self.slice.add_node(name=self.name, site=self.site.name)
        self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
        self.node.set_image(self.image)
        for iface in ifaces.keys():
            model = iface["model"]
            iface = self.node.add_compoment(model=model, name=name).get_interfaces()[0]
            iface["iface"]=iface

class L2Network:
    def __init__(self, slice, niclist=[]):
        self.name = name
        self.niclist = niclist
        self.slice.register_node(self)
        self.network = None
    
    def declare(self):
        self.network = self.slice.add_l2network(name=self.name, interfaces=niclist)

    def show(self):
        import pprint
        pprint.pprint(var(self))
        
        
#
#   use of this 
IMAGE = 'default_rocky_8'

s = Slice('MySliceSep12B')
node1 = Node(s, 'CMBS4Node_ncsa1', 'NCSA',
              disk=1, cores=2, ram=10, image=image)
node1.add_nic('NIC_Basic', 'GP') #general purpose NIC

node2 = Node(s, 'CMBS4Node_tacc2', 'TACC',
              disk=1, cores=2, ram=10, image=image)
node2.add_nic('NIC_Basic', 'GP') #general purpose NIC

net1 = L2Network(s, 'net1',[node1.get_iface("GP"), node2.get_face("GP")])

s.show()

#s.submit()
