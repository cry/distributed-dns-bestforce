# Distributed DNS Bruteforcer/Bestforcer

## Overview
Recon of hosts is essential for red teaming, and reveals targets which may contain vulnerabilities that may or may not exist on widely known hosts. One form of recon is subdomain guessing, where subdomains are permutated from a known wordlist and tested on whether they exist or not. Many tools exist to do this:

- altdns (https://github.com/infosec-au/altdns)
- sublist3r ([GitHub - aboul3la/Sublist3r: Fast subdomains enumeration tool for penetration testers](https://github.com/aboul3la/Sublist3r))

Once you have the list of subdomains, you need a way to resolve them. Again, there are a **ton** of tools for this:

- massdns ([GitHub - blechschmidt/massdns: A high-performance DNS stub resolver for bulk lookups and reconnaissance (subdomain enumeration)](https://github.com/blechschmidt/massdns))
- fernmelder (https://github.com/stealth/fernmelder)
- subbrute ([GitHub - TheRook/subbrute: A DNS meta-query spider that enumerates DNS records, and subdomains.](https://github.com/TheRook/subbrute))

It’s fine to run these tools alone on a single instance and they’ll generate good results, but the purpose of this something awesome is to **run these tools in a distributed manner**, which carries several benefits:

- It’s possible to scale up your brute forcing by simply adding more nodes to the swarm
- If Google doesn’t like you abusing their dns service, they can’t ban **all** of your slaves
- It’s a fun project

*Caveat: All the work done in this repository will be Docker based, as this is simply a PoC.*

## Architecture