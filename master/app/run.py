#!/bin/bash

import subgrabber
import argparse
import beanstalkc
import sys
import os
import re
import tempfile
import subprocess
import threading

def send(message):
    global dispatcher
    dispatcher.put(message.encode("zlib"))

def decode(res):
    return res.decode("zlib")

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Bestforcer : master')
    parser.add_argument('--domain', dest='domain', help='Domain to grab subdomains of', required=True)
    parser.add_argument('--broker', dest='broker', help='Broker to publish domains to', required=True)
    parser.add_argument('--blocksize', dest='blocksize', help='What size blocks of work to send to the broker', default=1000)

    args = parser.parse_args()

    blocksize = args.blocksize

    # Validate broker connection

    if not re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$', args.broker):
        print "[!] Broker DSN is invalid!"
        sys.exit(1)

    host, port = (lambda x: (x[0], int(x[1])))(args.broker.split(":"))

    print "[+] Connecting to %s:%s" % (str(host), str(port))

    dispatcher = beanstalkc.Connection(host=host, port=port)
    receiver = beanstalkc.Connection(host=host, port=port)

    dispatcher.use('jobs')
    receiver.watch('results')

    known_subdomains = subgrabber.run(args.domain)

    # Dump subdomains into tempfile

    (known_handle, known_filename) = tempfile.mkstemp()

    (altdns_handle, altdns_filename) = tempfile.mkstemp()

    print "[+] Writing known subdomains to %s, generated domain names to %s" % (known_filename, altdns_filename)

    os.fdopen(known_handle, "w").write("\n".join(known_subdomains))

    # Run altdns to generate more subdomains

    altdns_args = ["python", "altdns/altdns.py", "-i", known_filename, "-o", altdns_filename, "-w", "altdns/words.txt"]

    altdns = subprocess.Popen(altdns_args)

    altdns.wait()

    print "[+] altdns run finished, reading in generated domains"

    domains = open(altdns_filename, "r").read().split("\n")

    generated_count = len(domains)

    if not domains:
        print "[!] Retrieved domain count of 0, altdns failed somehow.."
        sys.exit(1)

    print "[+] Retrieved %d domains!" % generated_count

    blocks = chunks(domains, args.blocksize)

    for block in blocks:
        print "[+] Queued block of work"
        send("\0".join(block))

    while True:
        msg = receiver.reserve()

        print decode(msg.body)

        msg.delete()
