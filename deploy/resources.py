#!/usr/bin/env python3
"""

resrouces.py

Check that there are resources availbale for testing


More information is in the README, here:
https://github.com/CMB-S4/fabric_investigation

"""

import argparse
import subprocess
import logging
import os
import sys

def check_resources(args): pass


if __name__ == "__main__":

    """Create command line arguments"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=os.path.basename(sys.argv[0])
    )
    parser.add_argument('--loglevel', '-l',
                        help="Level for reporting e.g. WARN, ERROR, DEBUG",
                        default="INFO",
                        choices=["NONE", "WARN", "ERROR", "DEBUG"])
    parser.add_argument('--config', '-c',
                        help="configfile format file",
                        type=argparse.FileType('r'),
                        default="default.cfg",
                        )

    
    subparsers = parser.add_subparsers(help='supported operations:', dest='sub command listed above')
    subparsers.required = True
    
    chk_p = subparsers.add_parser('check', help='Check available resources')
    chk_p.add_argument('filename', type=str, help='Name of file of events to publish.')
    parser.add_argument("-f", "--format",
                        choices=["VOEVENT","CIRCULAR","BLOB"],
                        default="BLOB",
                        help="format of events")
    chk_p.set_defaults(func=check_resources)

    args = parser.parse_args()

    logging.basicConfig(level=logging.__dict__[args.loglevel])
    logging.debug("arguments are:{}".format(args))
    args.func(args)
    


