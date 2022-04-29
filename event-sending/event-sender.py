#!/usr/bin/env python3
"""
Post events and status to the Ssimma Hipskotch production instance. 

"""

epilog = """
OUr channel is cmb-s4-fabric-tests.phase-one-testing
Before use,
   - obtain an indentity and scram creential from my.hop.scimma.org
   - use "hop auth add" to store the credential
   - Ask Dn to put you in th eright group in scimma

to see what's been published:
 - hop subscribe kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing
Whant more? : A tutorial from SCIMMA is here
https://github.com/scimma/hop-client/wiki/Tutorial%3A-using-hop-client-with-the-SCiMMA-Hopskotch-server
"""
import argparse
import subprocess
import logging
import os
import sys

def send_file (args):
    cmd = "hop publish --format BLOB kafka://kafka.scimma.org/<your.topic> {}".format(args.filename)
    invoke_hop(cmd)

def send_status(args):
    cmd = "echo {} | hop publish --format BLOB kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing ".format(args.status_text)
    invoke_hop(cmd)

def invoke_hop(cmd):
    logging.info("about to run: {}".format(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    logging.info("Stdout  of Publish:{}".format(result.stdout))
    if result.returncode == 0 :
        logging.error("Could not publish Stderr:{}".format(result.stderr))
        exit(result.returncode)
        
if __name__ == "__main__":

    """Create command line arguments"""
    parser = argparse.ArgumentParser(
        description="__doc__",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=os.path.basename(sys.argv[0])
    )
    parser.add_argument('--loglevel', '-l',
                        help="Level for reporting e.g. WARN, ERROR, DEBUG",
                        default="INFO",
                        choices=["NONE", "WARN", "ERROR", "DEBUG"])
    parser.add_argument("-f", "--format",
                        choices=["VOEVENT","CIRCULAR","BLOB"],
                        default="BLOB",
                        help="format of messages")
    
    subparsers = parser.add_subparsers(help='supported operations:', dest='sub command listed above')
    subparsers.required = True
    
    pub_p = subparsers.add_parser('publish', help='Publish a file of events.')
    pub_p.add_argument('filename', type=str, help='Name of file of events to publish.')
    pub_p.set_defaults(func=send_file)
    
    status_p = subparsers.add_parser('status', help='send status passed via command line.')
    status_p.add_argument('status_text', type=str, help='Status text')
    status_p.set_defaults(func=send_status)

    args = parser.parse_args()
    logging.debug("arguments are:{}".format(args))
    
    logging.basicConfig(level=logging.__dict__[args.loglevel])

    args.func(args)
    


