#!/bin/bash

import argparse
import beanstalkc
import sys
import os
import re
import tempfile
import subprocess
import threading

def msg2block(msg):
    return msg.decode("zlib").split("\0")

def res2msg(res):
    return res.encode("zlib")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Bestforcer : slave')
    parser.add_argument('--broker', dest='broker', help='Broker to publish domains to', required=True)

    args = parser.parse_args()

    # Validate broker connection dsn

    if not re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$', args.broker):
        print "[!] Broker DSN is invalid!"
        sys.exit(1)

    host, port = (lambda x: (x[0], int(x[1])))(args.broker.split(":"))

    print "[+] Connecting to %s:%s" % (str(host), str(port))

    receiver = beanstalkc.Connection(host=host, port=port)
    dispatcher = beanstalkc.Connection(host=host, port=port)

    print "[+] Tubes available: " + " ".join(receiver.tubes())

    dispatcher.use('results')
    receiver.watch('jobs')

    devnull = open(os.devnull, 'w')

    while True:
        print "[+] Listening for messages.."

        job = receiver.reserve()

        print "[+] Got job from master!"

        block = msg2block(job.body)

        # Create a new temp file to store these domains to test

        (test_handle, test_filename) = tempfile.mkstemp()
        (res_handle, res_filename) = tempfile.mkstemp()

        print "[+] Writing block to " + test_filename + ", results to " + res_filename

        os.fdopen(test_handle, "w").write("\n".join(block))

        args = ["/massdns/bin/massdns", '-r', '/massdns/lists/resolvers.txt', '-t', 'A', '-w', res_filename, test_filename]

        massdns = subprocess.Popen(args, stdout=devnull, stderr=devnull)

        massdns.wait()

        print "[+] Finished processing block!"

        res = os.fdopen(res_handle, "r").read()

        dispatcher.put(res2msg(res))

        job.delete()
