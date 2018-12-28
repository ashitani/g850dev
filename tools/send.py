#!/usr/bin/env python
#coding: utf-8

from g850common import *

device='/dev/cu.usbserial-A62WWHTM'
delay = 50 #[msec/line]

if len(sys.argv)!=2:
    print("Usage: python send.py filename")
    quit()

filename=sys.argv[1]
send(filename, device, delay)

