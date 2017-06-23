#!/usr/bin/python

import argparse

#argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', help = "Port number", action="store", dest="p", required = True)
parser.add_argument('-m', help = "Mailing address", action="store", dest="m", required = True)
parser.add_argument('-r', help = "CSV filename", action="store", dest="r", required = True)
parser.add_argument('-c', help = "Cluster name", action="store", dest="c", required = True)
parser.add_argument('-d', help = "Dev mode", action="store", dest="d", required = True) # True|1 / False|0
args = parser.parse_args()

from webappSrc import *

port = args.p
email = args.m
csv = args.r
cluster = args.c
dev = args.d

csvInit(csv)
smtpInit(email)
setClusterName(cluster)
setDevMode(dev)

#nameCSVZipped = test() #in webappSrc.py
#print('#####:', nameCSVZipped)

run(host='localhost', port=port, debug=True)
