#!/bin/bash

docker run --name dnsbestforce_broker -d -p 11300:11300 dnsbestforce/beanstalkd "$@"
