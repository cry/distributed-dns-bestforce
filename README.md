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
![System Diagram](https://afire.io/cs6841/distributed.png)

The system is architected as such:

- The master receives a domain to brute force subdomains of
	- Optionally, it can try to retrieve known subdomains from either:
		- User input
		- Certificate transparency logs
		- DNSDumpster
- Once the master receives all the data it needs, it can operate in one of **two** modes
	- **Centralised generation**
		- The master generates the word list and segregate it into manageable blocks (50k per block?)
		- Slaves then receive these blocks from the message broker and operate on each of these blocks 
	- **Delegated generation**
		- The master creates parameters needed to generate the block of work
		- Slaves then receive these parameters and generate the wordlist locally
	- Delegated generation is useful in avoiding having the message broker as a bottleneck.
- Slaves receive blocks of work and then test all the domains contained within
- Results are sent back to the message broker, and hence the master
