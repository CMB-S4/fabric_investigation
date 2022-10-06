#!/usr/bin/env python
"""
Plan and provision resources in FABRIC.

"""

import argparse
import logging

#
# Utilities
#
def remove_py(string):
     # our convention is that slices and modules
     # are named but file name completeion in the
     # shell makes it eaty to submof the file name
     # instead of slice name, etc.
     if ".py" in string: string = string[:-3]
     return string

def print_help(args):
     "print help and exit"
     import sys
     args.parser.print_help(sys.stderr)
     exit(1)
          
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
     #import pdb; pdb.set_trace()
     importlib.invalidate_caches()
     #module = importlib.import_module(args.configuration, package=None)
     exec ("import {}".format(configuration))
     exec ("{}.apply()".format(configuration))

def delete(args):
     "delete a slice, if it exists"
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice_name = remove_py(args.slice_name)
     try:
          slice = fablib.get_slice(name=slice_name)
     except IndexError:
          logging.error(f"slice {slice_name} does not exist")
          exit(1)
     logging.info(f"about to delete slica named {slice_name}")
     slice.delete()

def _print(args):
     "Print information about nodes and networks in a slice"
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice_name = remove_py(args.slice_name)
     slice = fablib.get_slice(name=slice_name)
     print (f"{slice}")
     for node in slice.get_nodes():
          print (f"{node}")
     for net in slice.get_l3networks():
          print  (f"{net}")
     for net in slice.get_l2networks():
          print  (f"{net}")

def mass_execute(args):
     """
     Execute command(s) on all nodes in the slice.
     if the command begins with @ treat the argument as a file of commands.
     """
     def shorten (s):
          if len(s) > 50 : s = f"{s[:25]}...{s[-25]:}"
          return s
     
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice_name = remove_py(args.slice_name)
     slice = fablib.get_slice(slice_name)
     cmd = args.cmd
     if cmd[0] == "@" : cmd = open(cmd[1:],"r").read()
     abbreviated_cmd = shorten(cmd)
     if len(cmd) > 40 : abbreviated_cmd = f"{cmd[:20]}...{cmd[-20:]}"
     for node in slice.get_nodes():
          logging.info(f"{node} : {abbreviated_cmd}")
          stdout, stderr = node.execute(cmd)
          print (f"{node} stdout: {stdout}")
          if stderr: logging.info( f"{node} : stderr:{stderr}")

def cross_route(args):
     """
     Setup routes between all nodes so they can talk to each other
     """
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice_name = remove_py(args.slice_name)
     slice = fablib.get_slice(name=slice_name)
     import pdb; pdb.set_trace()
     nodes = slice.get_nodes()
     nets  = slice.get_l2networks()
     for net in nets:
          pass


def template(args):
     pass

def debug(args):
     "call a slice into memory and start the debugger"
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice_name = remove_py(args.slice_name)
     slice = fablib.get_slice(name=slice_name)
     import pdb; pdb.set_trace()

def slices(args):
     "print the name of all my slices"
     from fabrictestbed_extensions.fablib.fablib import fablib
     for slice in fablib.get_slices():
          print (slice.get_name())

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
     subparser.add_argument("slice_name", help = "slice_name")

     #print
     subparser = subparsers.add_parser('print', help=_print.__doc__)
     subparser.set_defaults(func=_print)
     subparser.add_argument("slice_name", help = "slice_name")

     #print
     subparser = subparsers.add_parser('mass_execute', help=mass_execute.__doc__)
     subparser.set_defaults(func=mass_execute)
     subparser.add_argument("slice_name", help = "slice_name")
     subparser.add_argument("cmd", help = "command")

     #cross_route
     subparser = subparsers.add_parser('cross_route', help=cross_route.__doc__)
     subparser.set_defaults(func=cross_route)
     subparser.add_argument("slice_name", help = "slice_name")

     #debug
     subparser = subparsers.add_parser('debug', help=debug.__doc__)
     subparser.set_defaults(func=debug)
     subparser.add_argument("slice_name", help = "slice_name")

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
