#!/usr/bin/env python3
"""

scimma_utils.py

Post events and messages  to the cmb-s4-fabric-tests.phase-one-testing
topic in the Scimma production instance. Allow for read-back for debugging 

Publish   -- sends a file of events, jsut as they are
             to SCiMMA infrastructure
Message   -- is intended to send operationsal status. Commandline text
             is wrapped in in JSON and Meta-Data added (time hostname, etc)
Subscribe -- reads the topic and dumps on stdout. The Edfaul is LATEST,
             meaning that if debugging, run this before pubishing or
             in the background.

More information is in the README, here:
https://github.com/CMB-S4/fabric_investigation

"""

import argparse
import subprocess
import logging
import os
import sys

def send_file (args):
    #Transmits a file of events to Hop.
    cmd = "hop publish --format {} kafka://kafka.scimma.org/<your.topic> {}".format(argas.format, args.filename)
    invoke_hop(cmd)

def send_message(args):
    #wrap ccommandline in a layer fo JOSN  and then publish
    import json
    import time
    import socket
    jstring = json.dumps({"time": time.time(),
                          "type": "message",
                          "ctime": time.ctime(),
                          "user":os.getlogin(),
                          "host": socket.gethostname(),
                          "message": args.message_text
                          }
                        )
    jstring = jstring.encode("utf-8") #subprocess requires a "byte stream"
    logging.info("full message json:{}",format(jstring))
    cmd = "hop publish --format BLOB kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing "
    logging.info("about to run: {}".format(cmd))
    result = subprocess.run(cmd,input=jstring, shell=True)
    logging.info("return status is: {}".format(result.returncode))
    exit (result.returncode)

def subscribe(args):
    #listen to the channel and print meassaages on standard out.
    cmd = "hop subscribe  -s {}  kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing".format(args.when)
    invoke_hop(cmd)

    
def invoke_hop(cmd):
    logging.info("about to run: {}".format(cmd))
    result = subprocess.run(cmd,  shell=True)
    logging.info("return status is: {}".format(result.returncode))
    exit(result.returncode)
        
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
    
    subparsers = parser.add_subparsers(help='supported operations:', dest='sub command listed above')
    subparsers.required = True
    
    pub_p = subparsers.add_parser('publish', help='Publish a file of events.')
    pub_p.add_argument('filename', type=str, help='Name of file of events to publish.')
    parser.add_argument("-f", "--format",
                        choices=["VOEVENT","CIRCULAR","BLOB"],
                        default="BLOB",
                        help="format of events")
    pub_p.set_defaults(func=send_file)
    
    message_p = subparsers.add_parser('message', help='send message passed via command line.')
    message_p.add_argument('message_text', type=str,
                        help='Message text, which is suppimented by meta data')
    message_p.set_defaults(func=send_message)

    sub_p = subparsers.add_parser('subscribe', help='subscribe to the test topic (to verify transmission')
    sub_p.add_argument("-w","--when", choices=["EARLIEST","LATEST"], default="LATEST",
                       help= "See all (EARLIEST)default, or wait for new stuff(LATEST)")
    sub_p.set_defaults(func=subscribe)
    

    args = parser.parse_args()

    logging.basicConfig(level=logging.__dict__[args.loglevel])
    logging.debug("arguments are:{}".format(args))
    args.func(args)
    


