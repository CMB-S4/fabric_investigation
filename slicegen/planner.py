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
     subparser = subparsers.add_parser('plan', help=list.__doc__)
     subparser.set_defaults(func=plan)
     subparser.add_argument("configuration", help = "configuration file")

     #instanitate
     subparser = subparsers.add_parser('apply', help=apply.__doc__)
     subparser.set_defaults(func=apply)
     subparser.add_argument("configuration", help = "configuration file")

     args = parser.parse_args()

     # translate text arguement to log level.
     # least to most verbose FATAL WARN INFO DEBUG
     # level also printst things to the left of it. 
     loglevel=logging.__dict__[args.loglevel]
     assert type(loglevel) == type(1)
     logging.basicConfig(level=logging.__dict__[args.loglevel])
     logging.info("args:{}".format(args))
     args.func(args)
