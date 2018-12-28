#!/usr/bin/env python
#coding: utf-8

from g850common import *

device='/dev/cu.usbserial-A62WWHTM'

txt=receive(device)
print(txt)
