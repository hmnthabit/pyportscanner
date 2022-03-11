# Author: hmsec
# Date: 2021-05-09

import argparse
import socket
import concurrent.futures

from termcolor import colored
from datetime import datetime

threads = []


def ports_list_scanner(host, ports, fout):
    '''Scans a list of ports '''

    # Get the host ip and the host name
    gethost(host)

    if ports:
        # Convert the ports string to a list
        ports = ports.split(",")
        # Launch threads of port_scan
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for port in ports:
                threads.append(executor.submit(
                    port_scan, host, int(port), port_dict, fout))
            concurrent.futures.wait(threads)
        print_results(threads, fout)


def port_range_scan(host, port_range, fout):
    '''
    Scan a specific range of ports
    '''
    gethost(host)

    if port_range:
        port_range = port_range.split(",")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for port in range(int(port_range[0]), int(port_range[1])+1):
                threads.append(executor.submit(
                    port_scan, host, int(port), port_dict, fout))
            
            concurrent.futures.wait(threads)

        print_results(threads, fout)

def port_scan(host, port, port_dict, fout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket.setdefaulttimeout(1)

    output = s.connect_ex((host, int(port)))

    if output == 0:
        result = "[+] Port {} is open --> {}\n".format(port, port_dict.get(port, "Unknown"))
        result2 = (colored("[+] Port {} is open --> {}".format(port,port_dict.get(port)), "green"),result)
        return result2

    else:
        result = "[+] Port {} is closed --> {}\n".format(port, port_dict.get(port, "Unknown"))
        result2 = (colored("[+] Port {} is closed --> {}".format(port, port_dict.get(port)), "red"),result)
        return result2


def common_ports_database():
    '''
    Read the ports and names from "common_ports.txt" and store them in `port_dict` dictionary
    '''
    port_dict = {}
    with open("./database/common_ports.txt", "r") as f:
        data = f.readlines()
        # data = data)
        for line in data:
            line = line.strip("\n").split("\t")
            port_dict[int(line[0])] = line[1]
    return port_dict

def print_results(threrads,fout):
                    
        if fout:
            # result will be printed in the same submitted order. However, the threads execution is asynchronous
            for b in (threads):
                r = b.result()
                print(r[0])
                fout.write(r[1])
        
        else:
            for b in (threads):
                r = b.result()
                print(r[0])
                # fout.write(r)

def gethost(host):
    # Get the host IP by the name
    try:
        host_ip = socket.gethostbyname(host)
    except socket.herror:
        print('[-] Cannot resolve {}'.format(host))
        return

    # Get the hostname by the IP
    try:
        host_name = socket.gethostbyaddr(host_ip)
        # Print the Host information
        print(
            '\n[+] Host info:\n Host Name: {}\n Host IP: {}'.format(host_name[0], host_ip))
    except socket.herror:
        print('[-] Cannot resolve {}'.format(host))
        return


def banner():
    print("""
  _____           _      _____                                  
 |  __ \         | |    / ____|                                 
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __  
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__| 
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |    
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|    
                                                                
                                                                
    """)


def arg_parser():
    # Initialize the parser object
    parser = argparse.ArgumentParser(
        usage='port_scanner.py -a HOST -p PORT1,PORT2'
        '\nExample 1: python3 port_scanner.py -a HOST -p 21,80'
        '\nExample 2: python3 port_scanner.py -a HOST --range 1,100 -o scan1.txt')

    # Add arguments
    parser.add_argument('-a', required=True, type=str,
                        metavar='HOST', help='Specify the target host')
    parser.add_argument('-p', type=str, metavar='PORTS',
                        help='Specify The target ports')
    parser.add_argument('--range', type=str,
                        help='Specify the port range e.g --range 100,200')
    parser.add_argument('-o', '--fout', action="store", type=str,
                        metavar='output_file', help='Specify the output file')

    args = parser.parse_args()

    # Specify meaningfull names to arguments
    args.host = args.a
    args.ports = args.p
    args.portrange = args.range
    args.fout = args.fout

    return args


if __name__ == "__main__":

    banner()
    # Parsing the arguments
    args = arg_parser()

    port_dict = common_ports_database()

    if args.fout:
        args.fout = open(args.fout, "w")

    if args.ports:
        t1 = datetime.now()
        ports_list_scanner(args.host, args.ports, args.fout)

        t2 = datetime.now()
        total = t2 - t1
        print("Finished in ", total)

    if args.portrange:
        t1 = datetime.now()
        port_range_scan(args.host, args.portrange, args.fout)

        t2 = datetime.now()
        total = t2 - t1
        print("Finished in ", total)

    # Close the file handle
    if args.fout:
        args.fout.close()
