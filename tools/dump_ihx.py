#!/usr/bin/env python
#coding: utf-8

from intelhex import IntelHex
import sys

filename=sys.argv[1]

data = IntelHex()
data.loadhex(filename)
data.dump()
