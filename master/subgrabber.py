#!/usr/bin/python

import argparse
import gatherers

parser = argparse.ArgumentParser(description='DNS Bestforcer : known subdomain grabber')
parser.add_argument('--domain', dest='domain', help='Domain to grab subdomains of', required=True)

args = parser.parse_args()

DOMAIN = args.domain

known_subdomains = set()

# Query crtsh

known_subdomains.update([f['name_value'].encode('utf-8') for f in gatherers.crtsh().search(DOMAIN)])

# Cool we've acquired our subdomains

print "\n".join(known_subdomains)
