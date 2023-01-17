#!/usr/bin/env python

"""
Plan and provision resources in FABRIC.

"""

import argparse
import logging
from pprint import *
from fabrictestbed_extensions.fablib.fablib import fablib
import pdb

#
# Utilities
#
def as_stem(string):
     # our convention is that slices and modules
     # are named but file name completeion in the
     # shell makes it easy to submit the a  name
     # of a file instead of slice name, 
     from pathlib import Path
     stem = Path(string).stem
     if stem[-1] == '.': stem = stem[:-1] 
     return f"{stem}"

def print_help(args):
     "print help and exit"
     import sys
     args.parser.print_help(sys.stderr)
     exit(1)

def get_slice(args):
     "get the slice whether by name or id"
     if args.id:
          slice = fablib.get_slice(slice_id=args.slice_name)
     else:
          name = as_stem(args.slice_name)
          try:     
               slice = fablib.get_slice(name)
          except IndexError:
               args.logger.error(f"slice {name} does not exist")
               exit(1)
     return slice

def get_logger(args):
     import logging
     import sys
     logger = logging.getLogger(sys.argv[0])
     loglevel=logging.__dict__[args.loglevel]
     assert type(loglevel) == type(1)
     logger.setLevel(level=loglevel)
     ch = logging.StreamHandler()
     ch.setLevel(level=loglevel)
     formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
     ch.setFormatter(formatter)
     logger.addHandler(ch)
     #logger.debug('debug message')
     #logger.info('info message')
     #logger.warning('warn message')
     #logger.error('error message')
     #logger.critical('critical message')
     return logger

class Digest:
     "provide interfaces to digest file" 
     def __init__(self, slice_name):
          self.slice_name = as_stem(slice_name)
          with open (self.slice_name + ".digest") as f : lines = f.read()
          
          #format is node<blank>ip-address\n
          lines = lines.split("\n")
          lines = [l.split(" ") for l in lines]
          lines = lines[:-1]
          self.names = [l[0] for l in lines]
          self.ips   = [l[1] for l in lines]
          args.logger.info(f"Digest file: {self.names}, {self.ips}")

     def get_names(self): return self.names

     def get_ips(self): return self.ips

     def get_names_ips(self) : return [z for z in zip(*[self.names, self.ips])]

#
#  end of utilities, beginning of command implementations
#
    
def plan(args):
     "show plan, but do not call FABRIC APIs "
     configuration = as_stem(args.configuration)
     exec ("import {}".format(configuration))
     exec ("{}.plan()".format(configuration))

def apply(args):
     "instantiate the plan by calling FABRIC APIs"
     configuration = as_stem(args.configuration)
     import importlib
     importlib.invalidate_caches()
     #module = importlib.import_module(args.configuration, package=None)
     exec ("import {}".format(configuration))
     exec ("{}.apply()".format(configuration))

def delete(args):
     "delete a slice, if it exists"
     slice = get_slice(args)
     args.logger.info(f"about to delete slica named {args.slice_name}")
     slice.delete()

def _print(args):
     "Print information about nodes and networks in a slice"
     slice_name = as_stem(args.slice_name)
     slice = get_slice(args)
     print (f"{slice}")
     for node in slice.get_nodes():
          print (f"{node}")
     for net in slice.get_l3networks():
          print  (f"{net}")
     for net in slice.get_l2networks():
          print  (f"{net}")

def _json(args):
     "emit json describing slice"
     import json
     slice = get_slice(args)
     slice_name = slice.get_name()
     net_list  = [{'name' : n.get_name(), 'layer' : f"{n.get_layer()}", 'site' : n.get_site()}
                  for n in slice.get_networks()]
     slice_info = {'slice_name' : slice_name, 'slice_id' : slice.slice_id }
     node_list = []
     for node in slice.get_nodes():
          node_info= {}
          node_info["name"] = node.get_name()
          node_info["site"] = node.get_site()
          addr_info = []
          for addr in node.ip_addr_list():
               details = [{'local':i['local'], 'family':i['family']} for i in addr['addr_info'] if i['scope'] == 'global']
               addr_info.append({'mtu': addr['mtu'], 'ifname' : addr['ifname'],
                                  'addr_info':details})
          node_info['addr'] = addr_info
          node_list.append(node_info)
     all_info = {"info" : {"slice" : slice_info, "networks" : net_list, "nodes" : node_list }}

     #Serialize and write.
     out = json.dumps(all_info, indent=2)
     if not args.file : args.file = f"{slice_name}.json"
     if "." not in args.file : args.file = args.file + ".json"
     with open(args.file, 'w') as jfile:
          jfile.write(out)
     args.logger.info(f"wrote {args.file}") 
     
def mass_execute(args):
     """
     Execute command(s) on all nodes in the slice.
     if the command begins with @ treat the argument as a file of commands.
     """
     def shorten (s):
          if len(s) > 50 : s = f"{s[:25]}...{s[-25]:}"
          return s
     
     slice = get_slice(args)
     cmd = args.cmd
     if cmd[0] == "@" : cmd = open(cmd[1:],"r").read()
     abbreviated_cmd = shorten(cmd)
     if len(cmd) > 40 : abbreviated_cmd = f"{cmd[:20]}...{cmd[-20:]}"
     for node in slice.get_nodes():
          args.logger.info(f"{node.get_name()} : {abbreviated_cmd}")
          print (f"{node.get_name()}")
          stdout, stderr = node.execute(cmd) # prints stdout (at least)
          print ()
          #print (f"{node.get_name()} stdout: {stdout}")
          if stderr: args.logger.info( f"{node.get_name()} : stderr:{stderr}")
     
def execute(args):
     "execute a command(s) on a specfic node"
     slice = get_slice(args)
     node  =slice.get_node(args.node_name)
     cmd = args.cmd
     if cmd[0] == "@" : cmd = open(cmd[1:],"r").read()
     stdout, stderr = node.execute(cmd)
     print (f"{stdout}")
     if stderr: args.logger.warn(f"stderr:{stderr}")
     

def health(args):
     "test topology health by having each node ping all the others"
     slice = get_slice(args)
     slice_name  = slice.get_name()
     digest = Digest(slice_name)
     n_errors = 0
     names_ips  = digest.get_names_ips()
     all_names = digest.get_names()
     args.logger.info(f"Node names:{all_names}")
     for this_name in all_names:
          cmds = [f"ping -c 2 {ip} > /dev/null ; echo $? # to {name}" for name, ip in names_ips]
          for cmd in cmds:
               args.logger.debug (f"trying on {this_name} : {cmd}")
               try:
                    (stdout, stderr) = slice.get_node(this_name).execute(f"{cmd}", quiet=True)
               except Exception as e:
                    args.logger.error("Exception", e)
                    print (f"{this_name} BROKEN {e.args}")
                    n_errors = n_errors + 1
               else:
                    args.logger.debug (f"{this_name} stdout: {stdout}") 
                    args.logger.debug (f"{this_name} stderr: {stderr}") 
                    if stdout == "0\n" :
                         status = "healthy"
                    else:
                         status = "BROKEN "
                         n_errors = n_errors + 1
               print (f"{this_name} {status} {cmd}")
     exit(n_errors)                 
     
def template(args):
     pass

def debug(args):
     "call a slice into memory and start the debugger"
     slice = get_slice(args)
     import pdb; pdb.set_trace()

def slices(args):
     "print the name of all my slices"
     for slice in fablib.get_slices():
          print (slice.slice_id, slice.get_name())

def resources(args):
     "experimental -- take a peek at resources"
     #import pdb; pdb.set_trace()
     manager = fablib.get_default_fablib_manager()
     if args.all :
          print(manager.list_sites())
     else:
          fields = ['Name', 'Hosts', 'CPUs', 'Cores Capacity','Cores Available']
          print(manager.list_sites(fields=fields, quiet=True))

def aliases (args):
     """
     Print out alias for ssh commands to each  node.
     Note that FABRIC nodes with IPV6 addresses cannot be
     reached from sites not supporting IPV6.

     "-u prints correponding unalias commands.

      """

     if not args.unalias:
          slice = get_slice(args)
          for node in slice.get_nodes():
               name = node.get_name()
               ip   = f"{node.get_management_ip()}"
               username = "rocky"
               print (f"alias {name}='ssh -F $FABRIC_SSH_CONFIGURATION_FILE -i $FABRIC_SLICE_PRIVATE_KEY_FILE {username}@{ip}'")
          return

     names = []
     try: 
          slice = get_slice(args)
          names  = [node.get_name() for node in slice.get_nodes()]
     except:
          args.logger.info("slice is gone, seeing if there is a digest")     
     if not names:
          digest = Digest(args.slice_name)
          names = [name for name in digest.get_names()]
          
     for name in names :print (f"unalias '{name}'")

def dns(args):
     """
     Setup /etc/hosts so all node can addess all others by name.
     These names can be made up and don't leak out of FABRIC.
     """
     slice = get_slice(args)
     digest = Digest(args.slice_name)
     subdomain = args.subdomain
     for this_name in digest.get_names():
          this_node = slice.get_node(this_name)
          for name, ip in digest.get_names_ips():
               if name == this_name: continue
               cmd = f"sudo bash -c 'echo {ip} {name}.{subdomain} >> /etc/hosts'"
               args.logger.info(f"executing {cmd} on {this_name}") 
               slice.get_node(this_name).execute(cmd)

def addr_show(args):
     """
     get low level status from all nodes
     """
     slice = get_slice(args)
     digest = Digest(args.slice_name)
     for name in digest.get_names():
          node = slice.get_node(name)
          stdout, stderr = node.execute("/usr.sbin/ip addr show")
          print (f"{name} {stdout}")

if __name__ == "__main__":

    #main_parser = argparse.ArgumentParser(add_help=False)
     parser = argparse.ArgumentParser(
          description=__doc__,
          formatter_class=argparse.RawDescriptionHelpFormatter)
     parser.add_argument('--loglevel','-l',
                             help='loglevel NONE, INFO,  DEBUG, ERROR, WARN',
                             default="INFO")
     parser.set_defaults(func=print_help)
   
     subparsers = parser.add_subparsers()   
 
     #list but not execute. 
     subparser = subparsers.add_parser('plan', help=plan.__doc__)
     subparser.set_defaults(func=plan)
     subparser.add_argument("configuration", help = "configuration file")

     #instanitate
     subparser = subparsers.add_parser('apply', help=apply.__doc__)
     subparser.set_defaults(func=apply)
     subparser.add_argument("configuration", help = "configuration file")

     #delete
     subparser = subparsers.add_parser('delete', help=delete.__doc__)
     subparser.set_defaults(func=delete)
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice_name")

     #print
     subparser = subparsers.add_parser('print', help=_print.__doc__)
     subparser.set_defaults(func=_print)
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice_name")

     #_json
     subparser = subparsers.add_parser('json', help=_json.__doc__)
     subparser.set_defaults(func=_json)
     subparser.add_argument("slice_name", help = "slice_name")
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     parser.add_argument('--file','-f',
                             help='output file Def slice_name.json',
                             default="")

     #mass_execute
     subparser = subparsers.add_parser('mass_execute', help=mass_execute.__doc__)
     subparser.set_defaults(func=mass_execute)
     subparser.add_argument("slice_name", help = "slice_name")
     subparser.add_argument("-i", "--id",  help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("cmd", help = "command")

     #execute
     subparser = subparsers.add_parser('execute', help=execute.__doc__)
     subparser.set_defaults(func=execute)
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice_name")
     subparser.add_argument("node_name", help = "node_name")
     subparser.add_argument("cmd", help = "command")
     

     #debug
     subparser = subparsers.add_parser('debug', help=debug.__doc__)
     subparser.set_defaults(func=debug)
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice name or id")

     #slices
     subparser = subparsers.add_parser('slices', help=slices.__doc__)
     subparser.set_defaults(func=slices)

     #resources
     subparser = subparsers.add_parser('resources', help=resources.__doc__)
     subparser.add_argument("-a", "--all",
                            help = "print all (e.g too many)resources",
                            action='store_true',  default=False)
     subparser.set_defaults(func=resources)

     #health
     subparser = subparsers.add_parser('health', help=health.__doc__)
     subparser.set_defaults(func=health)
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice name or id")

     #aliases
     subparser = subparsers.add_parser('aliases', help=aliases.__doc__)
     subparser.set_defaults(func=aliases )
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("-u", "--unalias", help = "unalias", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice name or id")

     #dns
     subparser = subparsers.add_parser('dns', help=dns.__doc__)
     subparser.set_defaults(func=dns )
     subparser.add_argument("-s", "--subdomain", help = "subdomian", default='fabric.cmbs4.org')
     subparser.add_argument("-i", "--id", help = "slice is an ID, not a name", action='store_true',  default=False)
     subparser.add_argument("slice_name", help = "slice name or id")

     args = parser.parse_args()
     args.logger = get_logger(args)
     

     args.logger.info("args:{}".format(args))
     args.parser = parser  #for help printer
     args.func(args)
