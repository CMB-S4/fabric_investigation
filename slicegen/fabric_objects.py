
image = "rockyLinux"

def show(object):
        types = [type(1),type(None),type(True),type(""), type(1.0) ]
        import pprint
        items = vars(object)
        print (items["name"])
        for (key, value) in items.items():
            if key == "name" : continue
            if type(value) in types:
                print ("  {}:{}".format(key, value))
            elif type(value) == type([]):
                    print("   {} {}".format(key, [v.name  for v in  value]))
            elif  type(value) == type({}):
                    print("   {} {}".format(key, value.keys()))
             
            

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
        show(self)
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
        self.nics = {}
        self.image = None
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

    def show(self):
        show(self)

    def declare():
        self.node = self.slice.add_node(name=self.name, site=self.site.name)
        self.node.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
        self.node.set_image(self.image)
        for nic in self.nics.keys():
            nic.iface = self.node.add_component(nic.model, nic.name).get_interfaces()[0]

class L2Network:
    def __init__(self, slice, name, niclist):
        self.name = name
        self.niclist = niclist
        self.slice = slice
        self.slice.register_network(self)
        self.network = None
    
    def declare(self):
        ilist = [n.iface for n in self.niclist]
        self.network = self.slice.add_l2network(name=self.name, interfaces=niclist)

        
    def show(self):
        show(self)


class Nic:
        def __init__ (self, node , name, model):
                self.name    = name
                self.model   = model
                self.node    = node
                self.iface   = None
        def show(self):
                show(self)

    
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

net1 = L2Network(s, 'net1',[node1.get_nic("GP"), node2.get_nic("GP")])

s.show()

#s.submit()
