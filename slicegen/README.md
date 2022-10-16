# CMBS-4 Phase on fabric invesitation FABRIC tools.
## Configuration  Language

Pythin is used as a configuration langaugrs

## Planner.py

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
arguement reuires a slice name and a .py (or any other file type
extention is suppled), the extention is ignored). This feature suports
shell commandline completion environamente. However, ti  convention
limits configuration  file names to valid python module names.

## Quickstert

### Install Supporting FABRIC libraries

```
$ python --version
Python 3.9.14
$ pip install fabrictestbed
$ pip install fabrictestbed-extensions
... clone this moudule from GIT```
```

### Get FABRIC Credentials

1. Ask Don or Greg to onboard you to the "CMB-S4 Phase one project"

2. Make a directory to hold the credentials you will make and download 

3. go to https://portal.fabric-testbed.net/experiments

4. floow link  to "Create Slice in Portal"

5. select "MANAGE SSH KEYS"

6. Select Key Type "sliver".  Generate and download keys. Save into your direcory.

7. Select Keytype  "bastion".  Generate and download keys. Save into your diretory

8. Generate a Token (a bit maddening. try manually reload screen).

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

### Instantiate the template configuration and play with the instanitaton.

Makes sure you have installed FABRC SSH keyss and recently obtained
a token from FABRIC.

```
./planner.py plan          template            # is the template what you owant?
./planner.py apply         template            # go make it in FABRIC.
./planner.py print         tempplate           # look at the instantiate conficuraiotn
./planner.py mass_execute  template  hostname  # run  hte hostnbame command  on all nodes
./planner.py json                              # get copius inforamtion about  your slice.
./plannerpy  delete        template            # tear d down what you madke
```


