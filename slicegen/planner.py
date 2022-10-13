#!/usr/bin/env python

"""
Plan and provision resources in FABRIC.

"""

import argparse
import logging
from pprint import *
from fabrictestbed_extensions.fablib.fablib import fablib

#
# Utilities
#
def remove_py(string):
     # our convention is that slices and modules
     # are named but file name completeion in the
     # shell makes it easy to submit the a  name
     # of a file instead of slice name, 
     from pathlib import Path
     stem = Path(string).stem
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
          name = remove_py(args.slice_name)
          try:     
               slice = fablib.get_slice(name)
          except IndexError:
               logging.error(f"slice {name} does not exist")
               exit(1)
     return slice
#   
#                
def plan(args):
     "show plan, but do not call FABRIC APIs "
     configuration = remove_py(args.configuration)
     exec ("import {}".format(configuration))
     exec ("{}.plan()".format(configuration))

def apply(args):
     "instantiate the plan by calling FABRIC APIs"
     configuration = remove_py(args.configuration)
     import importlib
     importlib.invalidate_caches()
     #module = importlib.import_module(args.configuration, package=None)
     exec ("import {}".format(configuration))
     exec ("{}.apply()".format(configuration))

def delete(args):
     "delete a slice, if it exists"
     slice = get_slice(args)
     logging.info(f"about to delete slica named {args.slice_name}")
     slice.delete()

def _print(args):
     "Print information about nodes and networks in a slice"
     slice_name = remove_py(args.slice_name)
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
     logging.info(f"wrote {args.file}") 
     
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
          logging.info(f"{node} : {abbreviated_cmd}")
          stdout, stderr = node.execute(cmd)
          print (f"{node}")
          print (f"stdout: {stdout}")
          if stderr: logging.info( f"{node} : stderr:{stderr}")

     
def execute(args):
     "execute a command(s) on a specfic node"
     slice = get_slice(args)
     node  =slice.get_node(args.node_name)
     cmd = args.cmd
     if cmd[0] == "@" : cmd = open(cmd[1:],"r").read()
     stdout, stderr = node.execute(cmd)
     print (f"{stdout}")
     if stderr: logging.warn(f"stderr:{stderr}")
     
          
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

     

     args = parser.parse_args()

     # translate text arguement to log level.
     # least to most verbose FATAL WARN INFO DEBUG
     # level also printst things to the left of it. 
     loglevel=logging.__dict__[args.loglevel]
     assert type(loglevel) == type(1)
     logging.basicConfig(level=logging.__dict__[args.loglevel])
     logging.info("args:{}".format(args))
     args.parser = parser
     args.func(args)
