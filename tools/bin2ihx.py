#!/usr/bin/env python
#coding: utf-8

from intelhex import IntelHex
import sys

args=sys.argv
if (len(args)!=3):
    print("Usage python bin2ihx.py [binfile] [offset]")

filename=sys.argv[1]
offset=eval(sys.argv[2])

data = IntelHex()

data.loadbin(filename,offset=offset)
outname=filename.replace(".bin",".ihx")

with open(outname,"w") as fw:
    data.write_hex_file(fw)

