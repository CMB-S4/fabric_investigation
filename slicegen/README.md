# CMBS-4 Phase one fabric invesitation FABRIC tools.

## Overview
The CMB-S4 phase one use case is to "inflate" a system, demonstrate
data flows and processing, then tear the system down. Modifying
a running  system using fabric_objects is not in the use case.  When
the demonstraton is done, we must tear the system  down.

In FABRIC, a unit of provisioning is a *slice*.  For CMB-S4 a slice is
a collection of nodes and networks.  A FABRIC site contains nodes
and networks. Routes between site networks allow data to be sent
between nodes on differnet sites.

fabric_objects allow CMB-S4 to create and use a topology of nodes and
networks supporting the project's "prompt" use case. Four kinds of
objects are used to instantiate FABRIC resources: 1)A CfSlice object
collects all other objects, invode the object's methods, and
represents the notion of slice within FABRIC 2) A CfNode objects
describe nodes.  3)The CfNetwork objects describe networks. In FABRIC.
a network is the network withing a site. 4) CfNic objects describe how
nodes connect to networks. Additionally, CfCmds objects send commands
to nodes.  (however use planner.py to send large number of commands to
nodes)

A file of python object declarations is the configuration file. For
an example, see the quickstart section, below. A Configuration file
specifies a slice,  and any number of network, node and nic objects.
The configuration file processing program , *planner.py* will import
the configuration file and cause the objects to be instantated.

"Plan level" prints out, in human readable form, a good deal of
information about what would be instantiated. This output helps an
author determine whether the configuration is what was intended, and can
serve to document the configuration.  Planning does not allocate
resources in FABRIC, and does not cause any FABRIC API's to be called.
i.e. A user running at Plan level need not be credentialed to access
FABRIC.

"Apply level" repeats the steps of planning, and then calls FABRIC
APIS to instantiate the plan. A slice object is instantiated,
nodes, then networks are declared to FABRIC. Information in
CfNic objects is used to connect nodes to site networks. Routes
are setup allowing all nodes to talk to all other nodes. Finally,
commands are issued in the order they have been declared.


## Object Declations

### CfSlice(name, **kwargs)
Collect the nodes and networks for a slice.                                                                                          
                                                                                                                                         
When planning cause the objects  to print information.                                                                               

When applying, cause the objects to make relevent calls                                                                            
to the FABRIC APIS. When all objects are processed, wait
for *delay* seconds before calling  *submit*.                                                                                        


Positional arguments:

```
    - name -- any ascii name for the slice. By convention,
      use __FILE__.
```

Keyword arguments:

```
    - delay -- seconds to delay before calling submit.
    
```

### CfNode (slice, name, image, **kwargs)

Create a Node, and specify non-network resources for the node.

Positional arguments:
```
slice  - slice object
name   - unique human-readbale name of node
image  - Operating system image to load on node
```

Keyword arguments:
```
     - cores -- Number of cores for node (def 20)
     - ram   -- GB of ram for the node   (def 40)
     - disk  -- GB of Disk for the node  (def 100)
     - site  -- FABRIC site for the node.(def NCSA)
```

### CfL3Network (slice, name, image, **kwrgs)

     Create a IPV4 L3 network.

Positional arguments:
```
     slice  - slice object
     name   - unique human-readbale name of node
     image  - Operating system image to load on node
```

Keyword arguments:
```
     None yet (type == IPV4, IPV6 envisioned)
```

### CfNIC (cfslice,  name,  cfnode, cfnetwork, **kwargs)

     Bind a  Network interface card to a node and  network

Positional arguments:
```
     cfslice         - slice object owning the NIC
     name            - unique human-readable name of NIC
     cfnode          - node object NIC is associated with
     cfnetwork       - network object NIC is associated with
```

Keyword arguments:
```
     - model -- NIC model (def NIC_Basic))
     - mtu   -- max packet size (def = 1500)
```


## Planner.py

A driver program, planner.py reads the python configuration files,
and starts the "plan", "apply" functions.  planner.py also performs
other operations, as indicated below.


```
usage: planner.py [-h] [--loglevel LOGLEVEL] {plan,apply,delete,print,json,mass_execute,execute,debug,slices,sites} ...

Plan and provision resources in FABRIC.

positional arguments:
  {plan,apply,delete,print,json,mass_execute,execute,debug,slices,sites}
    plan                Show plan, but do not call FABRIC APIs
    apply               Instantiate the plan by calling FABRIC APIs
    delete              Delete a slice, if it exists
    print               Print information about nodes and networks in a slice
    json                Emit json describing slice
    mass_execute        Execute command(s) on all nodes in the slice. If the
                        command begins with @ treat the argument as a file of
                        commands.
    execute             Execute a command(s) on a specfic node. If the command
                        begins with @ treat the argument as a file of commands.
                        The node is named by its name as known to fabric.
    debug               Call a slice into memory and start the debugger
    slices              Print the name of all my slices
    sites               Print the list of FABRIC resouroces at each site.

optional arguments:
  -h, --help            show this help message and exit
  --loglevel LOGLEVEL, -l LOGLEVEL
                        loglevel NONE, INFO, DEBUG, ERROR, WARN

```

By convention, slice names are named by the python configuration file
used to create them. For example template.py would be used to create a
slice named template.  Planner.py supports this convention when the
argument requires a slice name and a .py (or any other file type
extention is suppled), the extention is ignored). This feature suports
shell commandline completion environments. However, this  convention
limits configuration file names to valid python module names.


## Quickstart

### Install Supporting FABRIC libraries

```
$ python --version
Python 3.9.14
$ pip install fabrictestbed
$ pip install fabrictestbed-extensions
... clone this moudule from GIT```
```

### Get FABRIC Credentials

1. Ask Don or Greg to onboard you to the "CMB-S4 Phase one project."

2. Make a directory to hold the credentials you will make and download. 

3. go to https://portal.fabric-testbed.net/experiments.

4. follow link  to "Create Slice in Portal."

5. select "MANAGE SSH KEYS."

6. Select Key Type "sliver".  Generate and download keys. Save into your direcory.

7. Select Key Type  "bastion". Generate and download keys. Save into your diretory.

8. Generate a Token (try manually reloading screens, if needed).

9. Download token, Save into your directory.  Be prepared to generate a new token each working day.


Make a script analogue to this one and source it.

```
export FABRIC_PROJECT_ID='bfc7d97b-ac63-48d3-976e-2d344533b108'
export FABRIC_BASTION_HOST='bastion-1.fabric-testbed.net'
export FABRIC_CREDMGR_HOST='cm.fabric-testbed.net'
export FABRIC_ORCHESTRATOR_HOST='orchestrator.fabric-testbed.net'

export FABRIC_BASTION_USERNAME='petravic_0019236276'

export FABRIC_TOKEN_LOCATION='/Users/donaldp/.fabric/id_token.json'

export FABRIC_BASTION_KEY_LOCATION='/Users/donaldp/.fabric/fabric-bastion-key1'
export FABRIC_BASTION_PRIVATE_KEY_LOCATION='/Users/donaldp/.fabric/fabric-bastion-key1'
export FABRIC_BASTION_PUBLIC_KEY_LOCATION='/Users/donaldp/.fabric/fabric-bastion-key1.pub'

export FABRIC_SLICE_PRIVATE_KEY_FILE='/Users/donaldp/.fabric/fabric-sliver-key1'
export FABRIC_SLICE_PUBLIC_KEY_FILE='/Users/donaldp/.fabric/fabric-sliver-key1.pub'

```

### Copy this configuration into template.py
``` 
# default quantities for our nodes.                                                                                                      
image = 'default_rocky_8'
cores = 32
ram = 128
disk = 100

slice = CfSlice(__name__)
node1 = CfNode(slice, 'CMBS4Node1', image,
                disk=disk, cores=cores, ram=ram, site='TACC')
net1 = CfL3Network(slice, 'net1')


node2 = CfNode(slice, 'CMBS4Node2', image,
                disk=disk, cores=cores, ram=ram, site='NCSA')
net2 = CfL3Network(slice, 'net2')

CfNic(slice, "Node1.NIC1", node1, net1)
CfNic(slice, "Node2.NIC1", node2, net2)

def plan(): slice.plan()
def apply():slice.apply()
```

### Instantiate the template configuration and play with the instantiation.

Make sure you have installed FABRIC SSH keys and recently obtained
a token from FABRIC.

```
./planner.py plan          template            # is the template what you owant?
./planner.py apply         template            # go make it in FABRIC.
./planner.py print         template            # look at the instantiated configuraiotn
./planner.py mass_execute  template  hostname  # runthe "hostname" command  on all nodes
./planner.py json                              # get machine-readable information about your slice.
./plannerpy  delete        template            # tear down what you made
```

```

