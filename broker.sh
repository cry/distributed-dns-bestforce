#!/bin/bash

# Run script for broker

docker run -d -p 11300:11300 dnsbestforce/beanstalkd --name dnsbestforce_broker
