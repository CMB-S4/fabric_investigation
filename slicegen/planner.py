#!/usr/bin/env python
"""
Plan and provision resources in FABRIC.

"""

import argparse
import logging

#
#   
#                
def plan(args):
     #show plan, but do instantiate stuff.
     if ".py" in args.configuration:
          args.configuration = args.configuration[:-3]
     exec ("import {}".format(args.configuration))
     exec ("{}.plan()".format(args.configuration))

def apply(args):
     if ".py" in args.configuration:
          args.configuration = args.configuration[:-3]
     import importlib
     #import pdb; pdb.set_trace()
     importlib.invalidate_caches()
     #module = importlib.import_module(args.configuration, package=None)
     exec ("import {}".format(args.configuration))
     exec ("{}.apply()".format(args.configuration))

def delete(args):
     from fabrictestbed_extensions.fablib.fablib import fablib
     try:
          slice = fablib.get_slice(name=args.slice_name)
     except IndexError:
          logging.error(f"slice {args.slice_name} does not exist")
          exit(1)
     logging.info(f"about to delete slica named {args.slice_name}")
     slice.delete()

def _print(args):
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice = fablib.get_slice(name=args.slice_name)
     print (f"{slice}")
     for node in slice.get_nodes():
          print (f"{node}")
     for net in slice.get_l3networks():
          print  (f"{net}")
     for net in slice.get_l2networks():
          print  (f"{net}")
     import pdb; pdb.set_trace()

def mass_execute(args):
     """
     Execute command(s) on all nodes in the slice.
     if the command begins with @ treat the argument as a file of commands.
     """
     def shorten (s):
          if len(s) > 50 : s = f"{s[:25]}...{s[-25]:}"
          return s
     
     from fabrictestbed_extensions.fablib.fablib import fablib
     slice = fablib.get_slice(name=args.slice_name)
     cmd = args.cmd
     if cmd[0] == "@" : cmd = open(cmd[1:],"r").read()
     abbreviated_cmd = shorten(cmd)
     if len(cmd) > 40 : abbreviated_cmd = f"{cmd[:20]}...{cmd[-20:]}"
     for node in slice.get_nodes():
          logging.info(f"{node} : {abbreviated_cmd}")
          stdout, stderr = node.execute(cmd)
          print (f"{node} stdout: {stdout}")
          if stderr: logging.info( f"{node} : stderr:{stderr}")
          

def template(args):
     pass


if __name__ == "__main__":

    #main_parser = argparse.ArgumentParser(add_help=False)
     parser = argparse.ArgumentParser(
          description=__doc__,
          formatter_class=argparse.RawDescriptionHelpFormatter)
     parser.add_argument('--loglevel','-l',
                             help='loglevel NONE, "INFO",  DEBUG',
                             default="INFO")
     parser.set_defaults(func=parser.print_help)
   
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

     args = parser.parse_args()

     # translate text arguement to log level.
     # least to most verbose FATAL WARN INFO DEBUG
     # level also printst things to the left of it. 
     loglevel=logging.__dict__[args.loglevel]
     assert type(loglevel) == type(1)
     logging.basicConfig(level=logging.__dict__[args.loglevel])
     logging.info("args:{}".format(args))
     args.func(args)
