#!/usr/bin/python

import argparse
import gatherers

def run(domain=None):
    if not domain:
        raise Exception("You must provide a domain to scan")

    known_subdomains = set()

    known_subdomains.update([f['name_value'].encode('utf-8') for f in gatherers.crtsh().search(domain)])

    return list(known_subdomains)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Bestforcer : known subdomain grabber')
    parser.add_argument('--domain', dest='domain', help='Domain to grab subdomains of', required=True)

    args = parser.parse_args()

    DOMAIN = args.domain

    try:
        print "\n".join(run(DOMAIN))
    except:
        print ""
