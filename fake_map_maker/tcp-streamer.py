#!/usr/bin/env python3
"""
Send a rate-limited number of bytes each second on a TCP socket.
for each second, report the time to send a second's worth of bytes.
 or
Recieve data on a socket, and report the number of bytes
recieved each second.
"""

import time
import argparse
import logging
import tabulate
import socket


def send(args):
    """
    Send the requested bytes per second to the indicated IP
    addeess/port.

    Log tne time to send eaxh seconds worth of bytes.
    """
    host = args.host
    port = args.port
    buffer_size = args.buffer_size
    buffer = b'D'* buffer_size
    bytes_per_second = args.target_rate
    buffers_each_second = int(bytes_per_second/buffer_size)
    test_duration_seconds = args.duration
    logging.info("Host is:{}".format(host))
    if any(c.isalpha() for c in host) :
        host = socket.gethostbyname(host)
        logging.info("Host is:{}".format(host))
    logging.info("port is: {}".format(port))

    logging.info("Buffer_size,{:.5E} ".format(
        buffer_size))
    logging.info("requested rate (bytes/sec)  {:.5E}".format(
        bytes_per_second))
    logging.info("Number of buffers/sec  needed {:.5E}".format(
        buffers_each_second))
    logging.info("duration(Sec) 0 == infinaite{:.5E}".format(
        test_duration_seconds))

    
    with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #transfer the metered amount n a second ...
        # or report failure to compete on time
        s.connect((host, port))
        for iteration in range(test_duration_seconds):
            begin_time  = time.time() 
            for transfer in range (buffers_each_second):
                s.send(buffer)
            duration = time.time()  - begin_time
            logging.info("interation, duration: {}  {}".format(
                iteration, duration))
            if duration < 1: time.sleep(1-duration)
    

def recieve (args):
    """
    Recieve bytes on the indicated socket.
    Report the mumber of bytes recieved each second.
    """
    host = args.host
    port = args.port
    buffer_size = args.buffer_size
    
    logging.info("Host is: {}".format(host))

    #If DNS name translate to IP address. 
    if any(c.isalpha() for c in host) :
        host = socket.gethostbyname(host)
        logging.info("Host is:{}".format(host))
    logging.info("Port is: {}".format(port))
    logging.info("Recieve buffer sise is {}".format(buffer_size))
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind((host, port))
    serversocket.listen(5)
    (clientsocket, address) = serversocket.accept()
    logging.info("accepted connetion from: {}".format(address))

    #
    # Loop until sender closes file 
    #
    bytes_recieved = 0
    base_time = time.time()
 
    while True:
        bytes = clientsocket.recv(buffer_size)
        if not bytes:
           logging.info("Socket is closed, exiting")
           exit(0)
        bytes_recieved  += len(bytes)
        if time.time() - base_time  > 1 :
            logging.info("bytes  recieved in last second: {:,}".format( bytes_recieved))
            bytes_recieved = 0
            base_time = time.time()
        
if __name__ == "__main__":

    
    main_parser = argparse.ArgumentParser(
     description=__doc__,
     formatter_class=argparse.RawDescriptionHelpFormatter)
    main_parser.add_argument('--loglevel','-l',
                             help='loglevel INFO, ERROR, DEBUG etc. ',
                             default="INFO")
    main_parser.set_defaults(func=None) #if none then there no  subfunctions
    
    subparsers = main_parser.add_subparsers(title="subcommands",
                    description='valid subcommands',
                    help='additional help')

    #sender
    sub_parser = subparsers.add_parser('send',
                help=send.__doc__,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    sub_parser.set_defaults(func=send)
    sub_parser.add_argument(   "host",    help='IP addeess',
                                 default="127.0.0.1")
    sub_parser.add_argument(   "port",  help='port' , type=int, default=5000)
    sub_parser.add_argument('--target_rate','-r',
                             type=int,
                             help='target rate (bytes/sec)',
                             default=int(10E6))
    sub_parser.add_argument('--duration','-d',
                             type=int,
                             help='duration(sec)',
                             default=10)
    sub_parser.add_argument('--buffer_size','-b',
                             help='size of buffer to send or recv (bytes)',
                             type=int,
                             default=10000)


    #Reciever
    sub_parser = subparsers.add_parser('recieve',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                help=recieve.__doc__)
    sub_parser.set_defaults(func=recieve)
    sub_parser.add_argument(   "host",    help='IP addeess',
                                 default="127.0.0.1")
    sub_parser.add_argument(   "port",  help='port' , type=int, default=5000)
    sub_parser.add_argument('--buffer_size','-b',
                             help='size of buffer to send or recv (bytes)',
                             type=int,
                             default=10000)



    args = main_parser.parse_args()


    # translate text argument to log level.
    # least to most verbose FATAL WARN INFO DEBUG
    # level also printst things to the left of it. 
    loglevel=logging.__dict__[args.loglevel]
    assert type(loglevel) == type(1)
    logging.basicConfig(level=logging.__dict__[args.loglevel])

    logging.debug("arga:{}".format(args))
    if not args.func:  # there are no subfunctions
        main_parser.print_help()
        exit(1)
    args.func(args)

